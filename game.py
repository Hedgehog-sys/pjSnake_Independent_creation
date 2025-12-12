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
        self.game_over = False
        
        self.move_counter = 0
        self.move_delay = 3
        
        self.key_to_dir = {
            pygame.K_UP: (0, -CELL),
            pygame.K_DOWN: (0, CELL),
            pygame.K_LEFT: (-CELL, 0),
            pygame.K_RIGHT: (CELL, 0)
        }

        self.food.respawn(set(self.snake.segments + [self.snake.head]))
    
    def draw_grid(self):
        for i in range(0, SIZE, CELL):
            pygame.draw.line(self.screen, COLORS['grid'], (i, 0), (i, SIZE))
            pygame.draw.line(self.screen, COLORS['grid'], (0, i), (SIZE, i))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_SPACE and self.game_over:
                    self.__init__()

                if not self.game_over and event.key in self.key_to_dir:
                    dx, dy = self.key_to_dir[event.key]
                    self.snake.change_direction(dx, dy)
    
    def update(self):
        if not self.game_over:
            self.move_counter += 1
            if self.move_counter >= self.move_delay:
                self.move_counter = 0
                self.snake.move()

                if self.snake.head == self.food.pos:
                    self.snake.eat()
                    snake_body = set(self.snake.segments + [self.snake.head])
                    self.food.respawn(snake_body)

                if self.snake.check_collision():
                    self.game_over = True
    
    def draw(self):
        self.screen.fill(COLORS['bg'])
        self.draw_grid()

        for segment in self.snake.segments:
            pygame.draw.rect(self.screen, COLORS['snake'],
                           (segment[0], segment[1], CELL, CELL))

        pygame.draw.rect(self.screen, COLORS['snake'],
                        (self.snake.x, self.snake.y, CELL, CELL))
        pygame.draw.rect(self.screen, (0, 200, 0),
                        (self.snake.x, self.snake.y, CELL, CELL), 2)

        pygame.draw.rect(self.screen, COLORS['food'],
                        (*self.food.pos, CELL, CELL))

        font = pygame.font.SysFont(None, 30, bold=True)
        score_text = font.render(f"Очки: {self.snake.score}", 
                               True, COLORS['score'])
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            font = pygame.font.SysFont(None, 50, bold=True)
            text = font.render("GAME OVER", True, (255, 50, 50))
            text_rect = text.get_rect(center=(SIZE//2, SIZE//2 - 30))
            self.screen.blit(text, text_rect)
            
            font2 = pygame.font.SysFont(None, 25)
            text2 = font2.render("SPACE - рестарт", True, (200, 200, 50))
            text2_rect = text2.get_rect(center=(SIZE//2, SIZE//2 + 20))
            self.screen.blit(text2, text2_rect)
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)