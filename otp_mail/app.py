from flask import Flask, render_template, request, redirect, url_for, session, flash
import smtplib, ssl, random, time

app = Flask(__name__)
app.secret_key = "secret-key-demo"

otp_store = {}

# Cấu hình Gmail SMTP (đừng để pass thật công khai trong repo)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = "theunderdog0108@gmail.com"
SENDER_PASS = "wnzj nfva delj lsba"

def send_otp(email, code):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_PASS)
        message = f"""\
Subject: Your OTP Code

Your OTP is {code}. It will expire in 5 minutes."""
        server.sendmail(SENDER_EMAIL, email, message)

@app.route("/", methods=["GET", "POST"])
def index():
    # POST: user gửi email để nhận OTP
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        if not email:
            flash("Vui lòng nhập email.")
            return redirect(url_for("index"))

        code = str(random.randint(100000, 999999))
        otp_store[email] = {"code": code, "expires": time.time() + 300}

        try:
            send_otp(email, code)
            session["pending_email"] = email
            flash("OTP đã gửi về email. Nhập mã OTP để tiếp tục.")
            # PRG pattern: redirect sau POST
            return redirect(url_for("index"))
        except Exception as e:
            # nếu gửi lỗi, xóa record nếu đã tạo
            otp_store.pop(email, None)
            flash("Không gửi được email: " + str(e))
            return redirect(url_for("index"))

    # GET: nếu có pending_email trong session nhưng không có record (hoặc đã hết hạn) -> xoá
    pending = session.get("pending_email")
    if pending:
        record = otp_store.get(pending)
        if not record or time.time() > record["expires"]:
            otp_store.pop(pending, None)
            session.pop("pending_email", None)
            pending = None

    # truyền biến rõ ràng cho template
    return render_template("index.html", pending_email=pending)

@app.route("/verify", methods=["POST"])
def verify():
    email = session.get("pending_email")
    otp_input = request.form.get("otp", "").strip()

    if not email:
        flash("Chưa yêu cầu OTP.")
        return redirect(url_for("index"))

    record = otp_store.get(email)
    if not record:
        # không có record (server restart hoặc đã bị xóa)
        session.pop("pending_email", None)
        flash("Không tồn tại mã OTP. Vui lòng yêu cầu lại.")
        return redirect(url_for("index"))

    if time.time() > record["expires"]:
        otp_store.pop(email, None)
        session.pop("pending_email", None)
        flash("OTP đã hết hạn.")
        return redirect(url_for("index"))

    if otp_input == record["code"]:
        session["user"] = email
        otp_store.pop(email, None)
        session.pop("pending_email", None)
        flash("Đăng nhập thành công!")
        return redirect(url_for("welcome"))
    else:
        flash("Sai OTP.")
        return redirect(url_for("index"))

@app.route("/welcome")
def welcome():
    if "user" not in session:
        flash("Vui lòng đăng nhập trước.")
        return redirect(url_for("index"))
    return render_template("welcome.html", user=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    flash("Đã logout.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
