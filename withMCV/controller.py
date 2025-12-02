import random
import threading
from tkinter import messagebox

class PuzzleController:
    def __init__(self, model, view, player_name):
        self.model = model
        self.view = view
        self.player = player_name
        self.timer_seconds = 0
        self.first_click = None
        self.image_refs = []  
        self.tile_ids = {}

    def start_game(self):
        tiles, positions = self.model.load_and_cut()
        random.shuffle(positions)

        self.tile_ids, self.image_refs = self.view.show_tiles(
            tiles, self.model.grid_size,
            self.model.tile_w, self.model.tile_h,
            positions
        )

        
        self.view.canvas.bind("<Button-1>", self.on_click)
        self.update_timer()

    def update_timer(self):
        self.timer_seconds += 1
        self.view.timer_label.config(text=f"Time: {self.timer_seconds}s")
        self.view.root.after(1000, self.update_timer)

    def on_click(self, event):
        clicked = self.view.canvas.find_closest(event.x, event.y)[0]
        if self.first_click is None:
            self.first_click = clicked
            return

        
        x1, y1 = self.view.canvas.coords(self.first_click)
        x2, y2 = self.view.canvas.coords(clicked)
        self.view.canvas.coords(self.first_click, x2, y2)
        self.view.canvas.coords(clicked, x1, y1)

        self.first_click = None
        self.model.add_move()

        if self.check_win():
            messagebox.showinfo(
                "برنده!", f"حرکت‌ها: {self.model.moves}\nزمان: {self.timer_seconds}s"
            )

    def check_win(self):
        for tile_id, (r, c) in self.tile_ids.items():
            x, y = self.view.canvas.coords(tile_id)
            if x != c * self.model.tile_w or y != r * self.model.tile_h:
                return False
        return True

    def save_online(self):
        threading.Thread(target=self._save_online_worker).start()

    def _save_online_worker(self):
        import requests
        content = f"{self.player} | Moves: {self.model.moves} | Time: {self.timer_seconds}"
        open("result.txt", "w", encoding="utf-8").write(content)
        files = {"file": open("result.txt", "rb")}
        try:
            requests.post("https://fastapiapp-bwlf.onrender.com/save_result", files=files)
            messagebox.showinfo("Done", "Saved online!")
        except:
            messagebox.showerror("Error", "Server error!")
