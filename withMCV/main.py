import tkinter as tk
from tkinter.simpledialog import askstring
from model import PuzzleModel
from view import PuzzleView
from controller import PuzzleController

WINDOW_SIZE = 600
GRID_SIZE = 3
IMAGE_FILE = "bleach.jpg"

root = tk.Tk()
root.title("Puzzle MVC")
player = askstring("Player", "نام؟") or "Player1"

model = PuzzleModel(IMAGE_FILE, GRID_SIZE, WINDOW_SIZE)
view = PuzzleView(root, WINDOW_SIZE)
controller = PuzzleController(model, view, player)

controller.start_game()

save_btn = tk.Button(root, text="ارسال آنلاین", command=controller.save_online)
save_btn.pack()

root.mainloop()
