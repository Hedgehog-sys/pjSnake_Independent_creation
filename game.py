import pygame
import sys
from config import *
from snake import *
from food import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SIZE, SIZE))
        pygame.display.set_caption("THE BEST SNAKE")
        self.clock = pygame.time.Clock()
        
        self.snake = Snake()
        self.food = Food()

        self.key_to_dir = {
            pygame.K_UP: (0, -CELL),
            pygame.K_DOWN: (0, CELL),
            pygame.K_LEFT: (-CELL, 0),
            pygame.K_RIGHT: (CELL, 0)
        }
    
    def draw_grid(self):
        for i in range(0, SIZE, CELL):
            pygame.draw.line(self.screen, COLORS['grid'], (i, 0), (i, SIZE))
            pygame.draw.line(self.screen, COLORS['grid'], (0, i), (SIZE, i))
    
    def run(self):
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    if e.key in self.key_to_dir:
                        dx, dy = self.key_to_dir[e.key]
                        self.snake.move(dx, dy)

                        if self.snake.pos == self.food.pos:
                            self.snake.eat()
                            self.food.respawn()

                        if self.snake.check_collision():
                            print(f"Игра окончена! Очки: {self.snake.score}")
                            pygame.quit()
                            sys.exit()

            self.screen.fill(COLORS['bg'])
            self.draw_grid()

            pygame.draw.rect(self.screen, COLORS['food'], 
                           (*self.food.pos, CELL, CELL))

            pygame.draw.rect(self.screen, COLORS['snake'], 
                           (*self.snake.pos, CELL, CELL))

            pygame.draw.rect(self.screen, (0, 200, 0), 
                           (*self.snake.pos, CELL, CELL), 2)

            font = pygame.font.SysFont('Arial', 30, bold=True)
            score = font.render(f"Очки: {self.snake.score}", True, COLORS['score'])
            self.screen.blit(score, (10, 10))
            
            pygame.display.flip()
            self.clock.tick(FPS)