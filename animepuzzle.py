import tkinter as tk
from tkinter import messagebox
import random
import os
import sys
from tkinter.simpledialog import askstring  # === new

# ======================== Save local
def save_result_locally(player, moves, time):
    with open("result.txt", "a", encoding="utf-8") as f:  # === changed to result.txt
        f.write(f"{player} | Moves: {moves} | Time: {time}\n")

# Try to import Pillow
try:
    from PIL import Image, ImageTk
except Exception:
    Image = None
    ImageTk = None

# ===== تنظیمات اصلی =====
WINDOW_SIZE = 600
GRID_SIZE = 3
IMAGE_FILE = "bleach.jpg"

# ===== پنجره اصلی =====
root = tk.Tk()
root.title("🌸 Anime Puzzle Quest 🌸" \
"amir shirkhodaeetari(python mft)")
root.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE + 200}")

# ===== Player name input === new
player_name = askstring("Player Name", "لطفاً نام خود را وارد کنید:")
if not player_name:
    player_name = "Player1"

# ===== متغیرها =====
moves = 0
first_click = None
tiles = []

# ===== Timer =====
seconds = 0
timer_label = tk.Label(root, text="Time: 0s", font=("Helvetica", 12))
timer_label.pack(pady=5)

def update_timer():
    global seconds
    seconds += 1
    timer_label.config(text=f"Time: {seconds}s")
    root.after(1000, update_timer)

# ===== بارگذاری تصویر =====
if not os.path.exists(IMAGE_FILE):
    messagebox.showerror("Image not found", f"Image '{IMAGE_FILE}' not found.")
    sys.exit(1)

if Image is None or ImageTk is None:
    messagebox.showerror("Missing dependency",
        "Install Pillow:\n\npip install pillow")
    sys.exit(1)

pil_full = Image.open(IMAGE_FILE).convert("RGBA")
pil_full = pil_full.resize((WINDOW_SIZE, WINDOW_SIZE), Image.LANCZOS)
tile_width = WINDOW_SIZE // GRID_SIZE
tile_height = WINDOW_SIZE // GRID_SIZE

# ===== ساخت قطعه‌ها =====
for row in range(GRID_SIZE):
    row_tiles = []
    for col in range(GRID_SIZE):
        box = (
            col * tile_width,
            row * tile_height,
            (col + 1) * tile_width,
            (row + 1) * tile_height,
        )
        tile = pil_full.crop(box)
        tk_tile = ImageTk.PhotoImage(tile)
        row_tiles.append(tk_tile)
    tiles.append(row_tiles)

# ===== Canvas =====
canvas = tk.Canvas(root, width=WINDOW_SIZE, height=WINDOW_SIZE)
canvas.pack()

# ===== مخلوط کردن پازل =====
positions = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)]
random.shuffle(positions)
tile_ids = {}

for r in range(GRID_SIZE):
    for c in range(GRID_SIZE):
        x0 = c * tile_width
        y0 = r * tile_height
        tile_image = tiles[positions[r*GRID_SIZE + c][0]][positions[r*GRID_SIZE + c][1]]
        tile_id = canvas.create_image(x0, y0, anchor='nw', image=tile_image)
        tile_ids[tile_id] = positions[r*GRID_SIZE + c]

# ===== بررسی پایان =====
def check_win():
    for tile_id, (r, c) in tile_ids.items():
        x, y = canvas.coords(tile_id)
        if x != c * tile_width or y != r * tile_height:
            return False
    return True

# ===== کلیک =====
def on_click(event):
    global first_click, moves
    clicked = canvas.find_closest(event.x, event.y)[0]

    if first_click is None:
        first_click = clicked
    else:
        x1, y1 = canvas.coords(first_click)
        x2, y2 = canvas.coords(clicked)
        canvas.coords(first_click, x2, y2)
        canvas.coords(clicked, x1, y1)
        first_click = None
        moves += 1

        if check_win():
            messagebox.showinfo("🎉 تبریک! 🎉",
                                f"پازل کامل شد!\nحرکت‌ها: {moves}\nزمان: {seconds}s")
            save_result_locally(player_name, moves, seconds)  # === use player_name

canvas.bind("<Button-1>", on_click)
update_timer()

# ======================== Save to FastAPI
import requests

FASTAPI_URL = "https://fastapiapp-bwlf.onrender.com/save_result"

def save_result():
    global moves, seconds, player_name

    content = f"Player: {player_name}\nMoves: {moves}\nTime: {seconds}s\nGrid: {GRID_SIZE}x{GRID_SIZE}\n\n"  # === new

    with open("result.txt", "a", encoding="utf-8") as f:
        f.write(content)

    messagebox.showinfo("ذخیره شد", f"نتیجه بازی {player_name} ذخیره شد. ارسال به سرور...")

    try:
        with open("result.txt", "rb") as f:
            files = {"file": f}
            response = requests.post(FASTAPI_URL, files=files)

        if response.status_code == 200:
            messagebox.showinfo("سرور", "نتیجه با موفقیت ارسال شد!")
        else:
            messagebox.showerror("خطا", response.text)

    except Exception as e:
        messagebox.showerror("خطا", f"{e}")

# ===== دکمه سیو =====
DISPLAY_URL = "https://fastapiapp-bwlf.onrender.com/download/result.txt"
save_button = tk.Button(root, text="💾 ذخیره نتیجه و ارسال به سرور",
                        font=("Helvetica", 12), command=save_result)
save_button.pack(pady=10)

import webbrowser

def open_link(event):
    webbrowser.open_new(DISPLAY_URL)

# ===== نمایش لینک =====
link_label = tk.Label(root, text=DISPLAY_URL, fg="blue", cursor="hand2")
link_label.pack()
link_label.bind("<Button-1>", open_link)



root.mainloop()


import sys, os

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS  # مسیر فایل‌های موقت PyInstaller
else:
    BASE_DIR = os.path.dirname(__file__)

IMAGE_FILE = os.path.join(BASE_DIR, "bleach.jpg")

