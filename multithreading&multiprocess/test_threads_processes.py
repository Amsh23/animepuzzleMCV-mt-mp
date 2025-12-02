"""
یک نمونه کامل و واقعی از:
1) Multi-threading برای کارهای I/O
2) Multi-processing برای کارهای CPU (پردازش عکس)

اجرا:
    python test_threads_processes.py
"""
#خب اینجا میادش از یه سایته که از هوش مصنوعی گرفتم کدشو میادش پازل طور میکنه چندین تا عکس رو میگیره خودش یکی میکنه و میشه دیدش که سریع تر ظاهرا و قوی تر کار میکنه مولتی پروسس ولی تار میشه عکسش و خب مولتی تردینگ هم میبینیم که چطوره و چطور کار میکنه برای پردازش های قوی تر مولتی پروسس بهتره خیلی و برای استافده کل هسته های سی پی یو و در پردازش های سنگین و بعدا در کلاس مشین لرنینگ و ... استفادش خیلی جالب میشه
"""این کد از یک سایت گرفته شده و با کمک هوش مصنوعی
چندین تصویر را به شکل پازل‌مانند کنار هم قرار می‌دهد.
نسخهٔ چندپردازشی (Multi-Processing) سریع‌تر و قوی‌تر کار می‌کند
و از تمام هسته‌های CPU استفاده می‌کند، هرچند ممکن است تصویر خروجی کمی تار شود.
همچنین می‌توان عملکرد نسخهٔ چندریسمانی (Multi-Threading) را هم دید.
استفاده از چندپردازشی برای پردازش‌های سنگین و بعدها در کلاس‌های یادگیری ماشین
کاربردهای جالبی دارد.
"""

import time
import requests
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from PIL import Image, ImageFilter
import os

# ===============================
# ۱. کارهای واقعی I/O  (Threading)
# ===============================

URLS = [
    "https://picsum.photos/400",
    "https://picsum.photos/500",
    "https://picsum.photos/600",
]

def download_image(url):
    """ دانلود واقعی عکس (I/O واقعی → مناسب Threading) """
    start = time.time()
    r = requests.get(url)
    filename = f"dl_{int(start)}.jpg"

    with open(filename, "wb") as f:
        f.write(r.content)

    return f"Downloaded {filename} in {time.time() - start:.2f}s"


# ===================================
# ۲. کار CPU واقعی (Multiprocessing)
# ===================================

def process_tile(tile_image_bytes, effect):
    """
    پردازش سنگین روی یک تکه از تصویر (CPU-bound → مناسب Multiprocessing)
    tile_image_bytes = بایت‌های تکه عکس
    effect = نوع فیلتر
    """
    img = Image.open(tile_image_bytes)

    if effect == "blur":
        processed = img.filter(ImageFilter.GaussianBlur(6))
    elif effect == "gray":
        processed = img.convert("L")
    else:
        processed = img

    # خروجی را در حافظه نگه می‌داریم
    from io import BytesIO
    output = BytesIO()
    processed.save(output, format="JPEG")
    output.seek(0)
    return output.read()


def split_image_into_tiles(image_path, tile_size=200):
    """
    عکس را به تکه‌های 200x200 می‌بُرد
    """
    img = Image.open(image_path)
    w, h = img.size
    tiles = []

    from io import BytesIO

    for y in range(0, h, tile_size):
        for x in range(0, w, tile_size):
            box = (x, y, x + tile_size, y + tile_size)
            tile = img.crop(box)
            bio = BytesIO()
            tile.save(bio, format="JPEG")
            bio.seek(0)
            tiles.append((bio, (x, y)))

    return tiles, (w, h)


def merge_tiles(tiles_data, size):
    """
    تکه‌های پردازش شده را دوباره کنار هم قرار می‌دهد
    """
    w, h = size
    final_img = Image.new("RGB", (w, h))

    for tile_bytes, pos in tiles_data:
        from io import BytesIO
        tile = Image.open(BytesIO(tile_bytes))
        final_img.paste(tile, pos)

    final_img.save("output_processed.jpg")
    return "Saved output_processed.jpg"


# ===============================
# اجرای مثال‌ها
# ===============================

def test_multithreading():
    print("\n=== TEST: Multi-Threading (Real I/O) ===")

    start = time.time()

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(download_image, url) for url in URLS]

        for f in concurrent.futures.as_completed(futures):
            print(f.result())

    print(f"Threading total: {time.time() - start:.2f}s")


def test_multiprocessing():
    print("\n=== TEST: Multi-Processing (Real CPU Work) ===")

    input_image = "sample.jpg"

    if not os.path.exists(input_image):
        print("ERROR: Put a sample.jpg next to this file!")
        return

    tiles, size = split_image_into_tiles(input_image)

    start = time.time()

    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(process_tile, bio, "blur") for bio, pos in tiles
        ]

        processed_tiles = []
        for fut, (_, pos) in zip(futures, tiles):
            processed_tiles.append((fut.result(), pos))

    merge_tiles(processed_tiles, size)

    print(f"Multiprocessing total: {time.time() - start:.2f}s")


# ===============================
# main
# ===============================
if __name__ == "__main__":
    print("Running all tests...\n")

    # تست threading واقعی
    test_multithreading()

    # تست multiprocessing واقعی
    test_multiprocessing()

    print("\nDONE!")
