from config import WINDOW_HEIGHT, WINDOW_WIDTH, CELL

class Snake:
    def __init__(self):
        start_x = (WINDOW_WIDTH // CELL // 2) * CELL
        start_y = (WINDOW_HEIGHT // CELL // 2) * CELL
        self.x = start_x
        self.y = start_y
        self.direction = (CELL, 0)
        self.segments = []
        self.score = 0
        self.foods_eaten = 0

    @property
    def head(self):
        return (self.x, self.y)

    def move(self):
        self.segments.insert(0, (self.x, self.y))
        if len(self.segments) > self.foods_eaten:
            self.segments.pop()
        dx, dy = self.direction
        self.x += dx
        self.y += dy

    def change_direction(self, dx, dy):
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.direction = (dx, dy)

    def eat(self):
        self.foods_eaten += 1
        self.score += 10
        if self.foods_eaten % 5 == 0:
            self.score += 50

    def check_collision(self):
        if not (0 <= self.x < WINDOW_WIDTH and 0 <= self.y < WINDOW_HEIGHT):
            return True
        if (self.x, self.y) in self.segments:
            return True
        return False