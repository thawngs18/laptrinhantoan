from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3, random
import vonage

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Vonage API (thay bằng API_KEY và API_SECRET của bạn)
VONAGE_API_KEY = "10a8f999"
VONAGE_API_SECRET = "pH0*lIQ%"
VONAGE_NUMBER = "VonageVirtualNumber"  # số Vonage bạn mua

client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
sms = vonage.Sms(client)

# ----- Database helper -----
DB_NAME = "sdt.db"

def init_db():
    """Tạo database nếu chưa tồn tại"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT UNIQUE NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ----- Routes -----
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    name = request.form["name"].strip()
    phone = request.form["phone"].strip()
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, phone) VALUES (?, ?)", (name, phone))
        conn.commit()
        conn.close()
        flash("Đăng ký thành công! Hãy login OTP.")
    except sqlite3.IntegrityError:
        flash("Số điện thoại đã tồn tại!")
    return redirect(url_for("index"))


@app.route("/login", methods=["POST"])
def login():
    phone = request.form["phone"].strip()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE phone=?", (phone,))
    user = cur.fetchone()
    conn.close()

    if not user:
        flash("Số điện thoại chưa đăng ký!")
        return redirect(url_for("index"))

    otp = str(random.randint(100000, 999999))
    session["otp"] = otp
    session["phone"] = phone
    session["name"] = user["name"]

    # Gửi OTP qua Vonage
    response = sms.send_message({
        "from": VONAGE_NUMBER,
        "to": phone,
        "text": f"Your OTP code is {otp}"
    })

    if response["messages"][0]["status"] == "0":
        flash("OTP đã được gửi đến số điện thoại của bạn!")
    else:
        flash("Không thể gửi OTP: " + response["messages"][0]["error-text"])
        return redirect(url_for("index"))

    return redirect(url_for("otp"))


@app.route("/otp", methods=["GET", "POST"])
def otp():
    if request.method == "POST":
        code = request.form["otp"]
        if "otp" in session and code == session["otp"]:
            return redirect(url_for("welcome"))
        else:
            flash("OTP không đúng, thử lại.")
            return redirect(url_for("otp"))

    return render_template("otp.html")


@app.route("/welcome")
def welcome():
    if "phone" not in session:
        return redirect(url_for("index"))
    return render_template("welcome.html", phone=session["phone"], name=session["name"])


if __name__ == "__main__":
    init_db()  # tạo DB khi app chạy lần đầu
    app.run(debug=True)
