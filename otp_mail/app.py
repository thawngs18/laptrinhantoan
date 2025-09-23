from flask import Flask, render_template, request, redirect, url_for, session, flash
import smtplib, ssl, random, time

app = Flask(__name__)
app.secret_key = "secret-key-demo"  


otp_store = {}

# Cấu hình Gmail SMTP
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
    if request.method == "POST":
        email = request.form["email"]
        code = str(random.randint(100000, 999999))
        otp_store[email] = {"code": code, "expires": time.time() + 300}
        try:
            send_otp(email, code)
            session["pending_email"] = email
            flash("OTP đã gửi về email. Nhập mã OTP để tiếp tục.")
        except Exception as e:
            flash("Không gửi được email: " + str(e))
    return render_template("index.html")

@app.route("/verify", methods=["POST"])
def verify():
    email = session.get("pending_email")
    otp_input = request.form["otp"]
    if not email or email not in otp_store:
        flash("Chưa yêu cầu OTP.")
        return redirect(url_for("index"))
    record = otp_store[email]
    if time.time() > record["expires"]:
        flash("OTP đã hết hạn.")
        otp_store.pop(email)
    elif otp_input == record["code"]:
        session["user"] = email
        otp_store.pop(email)
        flash("Đăng nhập thành công!")
    else:
        flash("Sai OTP.")
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    flash("Đã logout.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
