import random
from config import *

class Food:
    def __init__(self):
        self.x = self.y = 0
        self.respawn()

    def respawn(self):
        grid = SIZE // CELL
        self.x = random.randint(0, grid-1) * CELL
        self.y = random.randint(0, grid-1) * CELL

    @property
    def pos(self):
        return (self.x, self.y)