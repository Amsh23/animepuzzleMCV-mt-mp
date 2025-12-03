#ph.rafie@gmail.com
from dotenv import load_dotenv
import os
import yagmail
import zipfile
import shutil

load_dotenv()

sender = os.getenv("EMAIL_ADDRESS")
app_password = os.getenv("EMAIL_APP_PASSWORD")

receiver = "am.shiii2003@gmail.com"

# پوشه‌ای که نمی‌خواهیم در ZIP شامل شود
exclude_dirs = {'build', '__pycache__', '.git', '.env', '.venv', 'venv', '.pytest_cache'}
exclude_files = {'.pyc', '.pyo', '.gitignore', '.env'}

def create_compact_zip(project_root, output_zip):
    """ZIP فشرده‌تر بدون فایل‌های غیر ضروری"""
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for root, dirs, files in os.walk(project_root):
            # فیلتر پوشه‌های غیر ضروری
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                # فیلتر فایل‌های غیر ضروری
                if not any(file.endswith(ext) for ext in exclude_files):
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, project_root)
                    zipf.write(file_path, arcname)
    
    print(f"✓ ZIP ایجاد شد: {output_zip}")
    size_mb = os.path.getsize(output_zip) / (1024 * 1024)
    print(f"✓ اندازه فایل: {size_mb:.2f} MB")

# مسیر فایل پیوست
attachment_path = os.path.join(os.path.dirname(__file__), "project_compact.zip")
project_root = os.path.join(os.path.dirname(__file__), "..")

# ایجاد ZIP فشرده
create_compact_zip(project_root, attachment_path)

# بررسی اندازه فایل (حد Gmail: 25 MB)
file_size_mb = os.path.getsize(attachment_path) / (1024 * 1024)
if file_size_mb > 24:
    print(f"⚠ اخطار: فایل ({file_size_mb:.2f} MB) از حد Gmail (25 MB) نزدیک است!")

try:
    yag = yagmail.SMTP(sender, app_password)

    yag.send(
        to=receiver,
        subject="پروژه نهایی پایتون مجتمع فنی امیر شیرخدائی طاری",
        contents="""
سلام استاد،
پروژه کامل در فایل ZIP پیوست شده.

لینک گیت‌هاب پروژه:
https://github.com/Amsh23/animepuzzleMCV-mt-mp

موارد شامل:
- withMCV: پروژه MVC اصلی
- multithreading&multiprocess: تست Multi-Threading/Processing
- gmailsmtp: سیستم ارسال ایمیل

با تشکر
""",
        attachments=attachment_path
    )
    
    print("✓ ایمیل ارسال شد!")
    
except Exception as e:
    print(f"✗ خطا در ارسال: {e}")
    
finally:
    # پاک کردن فایل موقتی
    if os.path.exists(attachment_path):
        os.remove(attachment_path)
        print("✓ فایل موقتی پاک شد")
