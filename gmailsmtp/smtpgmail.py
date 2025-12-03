#ph.rafie@gmail.com
from dotenv import load_dotenv
import os
import yagmail

load_dotenv()

sender = os.getenv("EMAIL_ADDRESS")
app_password = os.getenv("EMAIL_APP_PASSWORD")

receiver = "am.shiii2003@gmail.com"


attachment_path = os.path.join(os.path.dirname(__file__), "project.rar")


if not os.path.exists(attachment_path):
    print(f"خطا: فایل {attachment_path} یافت نشد!")
    exit(1)

yag = yagmail.SMTP(sender, app_password)

yag.send(
    to=receiver,
    subject="پروژه نهایی پایتون مجتمع فنی امیر شیرخدائی طاری",
    contents="""
سلام استاد،
پروژه کامل در فایل ZIP پیوست شده.
لینک گیت‌هاب پروژه:
https://github.com/Amsh23/animepuzzleMCV-mt-mp
با تشکر
""",
    attachments=attachment_path
)

print("ایمیل ارسال شد!")
