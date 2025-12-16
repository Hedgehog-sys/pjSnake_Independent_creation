import random
from config import *

class Food:
    def __init__(self):
        self.x = 0
        self.y = 0

    def respawn(self, snake_body):
        grid_w = WINDOW_WIDTH // CELL
        grid_h = WINDOW_HEIGHT // CELL
        all_cells = [(x * CELL, y * CELL) for x in range(grid_w) for y in range(grid_h)]
        free_cells = [cell for cell in all_cells if cell not in snake_body]
        if free_cells:
            self.x, self.y = random.choice(free_cells)
        else:
            self.x, self.y = (0, 0)

    @property
    def pos(self):
        return (self.x, self.y)