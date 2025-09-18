from flask import Flask, render_template, request, redirect, url_for, session, flash
from itsdangerous import URLSafeTimedSerializer
import os, smtplib, sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Serializer để tạo token
s = URLSafeTimedSerializer(app.secret_key)

# Cấu hình Gmail SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "theunderdog0108@gmail.com"     
EMAIL_PASSWORD = "wnzj nfva delj lsba"  

# ================== DATABASE ==================
DB_FILE = "users.db"

def init_db():
    """Tạo DB nếu chưa có"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()
    conn.close()

def add_user(name, email):
    """Thêm user mới"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # email đã tồn tại thì bỏ qua
    conn.close()

def get_user(email):
    """Lấy user theo email"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    user = c.fetchone()
    conn.close()
    return user

# ================== SEND MAIL ==================
def send_magic_link(email, login_url):
    """Gửi email magic link"""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your Magic Login Link"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email

    html_content = f"""
    <html>
      <body>
        <p>Xin chào,<br>
           Bấm vào link để đăng nhập:<br>
           <a href="{login_url}">{login_url}</a>
        </p>
      </body>
    </html>
    """
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, email, msg.as_string())
        print(f"✅ Đã gửi magic link tới {email}")
    except Exception as e:
        print(f"⚠️ Lỗi khi gửi email: {e}\nLink: {login_url}")

# ================== ROUTES ==================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    email = request.form.get("email")

    if not name or not email:
        flash("Vui lòng nhập đầy đủ thông tin!")
        return redirect(url_for("index"))

    add_user(name, email)
    flash("Đăng ký thành công! Giờ bạn có thể login bằng Magic Link.")
    return redirect(url_for("index"))

@app.route("/send_link", methods=["POST"])
def send_link():
    email = request.form.get("email")
    user = get_user(email)

    if not user:
        flash("Email chưa đăng ký!")
        return redirect(url_for("index"))

    token = s.dumps(email, salt="magic-link")
    login_url = url_for("login_with_token", token=token, _external=True)

    send_magic_link(email, login_url)
    flash("Magic link đã được gửi! Kiểm tra email.")
    return redirect(url_for("index"))

@app.route("/login/<token>")
def login_with_token(token):
    try:
        email = s.loads(token, salt="magic-link", max_age=300)  # link sống 5 phút
    except Exception:
        flash("Link không hợp lệ hoặc đã hết hạn!")
        return redirect(url_for("index"))

    user = get_user(email)
    if not user:
        flash("Không tìm thấy user!")
        return redirect(url_for("index"))

    session["user"] = user[1]  # name
    return redirect(url_for("welcome"))

@app.route("/welcome")
def welcome():
    if "user" not in session:
        return redirect(url_for("index"))
    return render_template("welcome.html", user=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    flash("Bạn đã logout.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
