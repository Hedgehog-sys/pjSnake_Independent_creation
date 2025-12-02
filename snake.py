from config import *

class Snake:
    def __init__(self):
        center = SIZE // 2 // CELL * CELL
        self.data = [center, center, 0]
    
    @property
    def pos(self): 
        return (self.data[0], self.data[1])
    
    @property
    def score(self): 
        return self.data[2]
    
    def move(self, dx, dy): 
        self.data[0] += dx
        self.data[1] += dy
    
    def eat(self): 
        self.data[2] += 50
    
    def check_collision(self):
        x, y = self.pos
        return not (0 <= x < SIZE and 0 <= y < SIZE)