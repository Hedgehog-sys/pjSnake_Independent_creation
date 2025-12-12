from config import *

class Snake:
    def __init__(self):
        start_x = SIZE // 2 // CELL * CELL
        start_y = SIZE // 2 // CELL * CELL
        self.x = start_x
        self.y = start_y
        self.direction = (CELL, 0)
        self.score = 0
        self.segments = []
        for i in range(1, INITIAL_LENGTH):
            seg_x = start_x - i * CELL
            seg_y = start_y
            self.segments.append((seg_x, seg_y))
    
    @property
    def head(self):
        return (self.x, self.y)
    
    def move(self):
        current_pos = (self.x, self.y)
        self.segments.insert(0, current_pos)
        desired_length = INITIAL_LENGTH + self.score // 50

        if len(self.segments) > desired_length:
            self.segments.pop()
        dx, dy = self.direction
        self.x += dx
        self.y += dy
    
    def change_direction(self, dx, dy):
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.direction = (dx, dy)
    
    def eat(self):
        self.score += 50
    
    def check_collision(self):
        wall_collision = not (0 <= self.x < SIZE and 0 <= self.y < SIZE)
        body_collision = (self.x, self.y) in self.segments
        return wall_collision or body_collision