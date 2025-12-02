from PIL import Image

class PuzzleModel:
    def __init__(self, image_file, grid_size, window_size):
        self.image_file = image_file
        self.grid_size = grid_size
        self.window_size = window_size
        self.tile_w = window_size // grid_size
        self.tile_h = window_size // grid_size
        self.tiles = []
        self.positions = []
        self.moves = 0

    def load_and_cut(self):
        img = Image.open(self.image_file).convert("RGBA")
        img = img.resize((self.window_size, self.window_size))

        self.tiles = []
        for r in range(self.grid_size):
            row_tiles = []
            for c in range(self.grid_size):
                box = (
                    c * self.tile_w,
                    r * self.tile_h,
                    (c+1) * self.tile_w,
                    (r+1) * self.tile_h
                )
                row_tiles.append(img.crop(box))
            self.tiles.append(row_tiles)

        
        self.positions = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size)]
        return self.tiles, self.positions

    def add_move(self):
        self.moves += 1
