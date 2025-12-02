import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk

class PuzzleView:
    def __init__(self, root, window_size):
        self.root = root
        self.canvas = tk.Canvas(root, width=window_size, height=window_size)
        self.canvas.pack()
        self.timer_label = tk.Label(root, text="Time: 0s", font=("Helvetica", 12))
        self.timer_label.pack()

    def show_tiles(self, tile_images, grid_size, tile_w, tile_h, shuffled_positions):
        img_tiles = []
        ids = {}
        for r in range(grid_size):
            for c in range(grid_size):
                src_r, src_c = shuffled_positions[r * grid_size + c]
                t = ImageTk.PhotoImage(tile_images[src_r][src_c])
                img_tiles.append(t)
                tile_id = self.canvas.create_image(
                    c * tile_w, r * tile_h, anchor="nw", image=t
                )
                ids[tile_id] = (src_r, src_c)
        return ids, img_tiles
