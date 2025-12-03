# ph.rafie@gmail.com
from dotenv import load_dotenv
import os
import yagmail

load_dotenv()

sender = os.getenv("EMAIL_ADDRESS")
app_password = os.getenv("EMAIL_APP_PASSWORD")

receiver = "am.shiii2003@gmail.com"

# SMTP اتصال با جیمیل
yag = yagmail.SMTP(sender, app_password)

yag.send(
    to=receiver,
    subject="پروژه نهایی پایتون - مجتمع فنی امیر شیرخدائی طاری",
    contents=f"""
سلام استاد وقت بخیر،
به دلیل حجم بالای فایل پروژه، نسخه کامل داخل Google Drive قرار داده شده و از لینک زیر قابل دانلود است:

Google Drive Link:
https://drive.google.com/file/d/1ym2yypXj3cfUBEnrxPODttKN1BJXWoYY/view?usp=drive_link

لینک گیت‌هاب پروژه:
https://github.com/Amsh23/animepuzzleMCV-mt-mp

با تشکر و احترام
امیر شیرخدائی طاری
"""
)

print("ایمیل ارسال شد!")