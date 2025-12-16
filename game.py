# game.py
import pygame
import sys
import math
import os
from config import *
from snake import *
from food import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("THE BEST SNAKE")
        self.clock = pygame.time.Clock()

        self.snake = Snake()
        self.food = Food()
        self.game_over = False

        self.eat_sound = self.generate_beep(frequency=880, duration=0.1)
        self.crash_sound = self.generate_beep(frequency=110, duration=0.3)

        self.record = self.load_record()

        self.key_to_dir = {
            pygame.K_UP: (0, -CELL),
            pygame.K_DOWN: (0, CELL),
            pygame.K_LEFT: (-CELL, 0),
            pygame.K_RIGHT: (CELL, 0)
        }

        self.food.respawn(set(self.snake.segments + [self.snake.head]))

    def generate_beep(self, frequency, duration):
        sample_rate = 44100
        n_samples = int(round(duration * sample_rate))
        buf = bytearray()
        for i in range(n_samples):
            t = float(i) / sample_rate
            val = math.sin(2.0 * math.pi * frequency * t)
            sample = int(val * 32767)
            buf.extend(sample.to_bytes(2, byteorder='little', signed=True))
            buf.extend(sample.to_bytes(2, byteorder='little', signed=True))
        return pygame.mixer.Sound(buffer=bytes(buf))

    def load_record(self):
        if os.path.exists("record.txt"):
            try:
                with open("record.txt", "r") as f:
                    return int(f.read().strip())
            except:
                return 0
        return 0

    def save_record(self, score):
        with open("record.txt", "w") as f:
            f.write(str(score))

    def draw_grid(self):
        for x in range(0, WINDOW_WIDTH, CELL):
            pygame.draw.line(self.screen, COLORS['grid'], (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL):
            pygame.draw.line(self.screen, COLORS['grid'], (0, y), (WINDOW_WIDTH, y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if self.game_over and event.key == pygame.K_SPACE:
                    self.__init__()

                if not self.game_over and event.key in self.key_to_dir:
                    dx, dy = self.key_to_dir[event.key]
                    self.snake.change_direction(dx, dy)

    def update(self):
        if not self.game_over:
            self.snake.move()
            if self.snake.head == self.food.pos:
                self.snake.eat()
                self.food.respawn(set(self.snake.segments + [self.snake.head]))
                self.eat_sound.play()

            if self.snake.check_collision():
                self.game_over = True
                self.crash_sound.play()
                if self.snake.score > self.record:
                    self.record = self.snake.score
                    self.save_record(self.record)

    def draw(self):
        self.screen.fill(COLORS['bg'])
        self.draw_grid()

        for seg in self.snake.segments:
            pygame.draw.rect(self.screen, COLORS['snake'], (*seg, CELL, CELL))
        pygame.draw.rect(self.screen, COLORS['snake'], (self.snake.x, self.snake.y, CELL, CELL))
        pygame.draw.rect(self.screen, COLORS['food'], (*self.food.pos, CELL, CELL))

        font = pygame.font.SysFont(None, 30, bold=True)
        score_text = font.render(f"Очки: {self.snake.score}", True, COLORS['score'])
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            font1 = pygame.font.SysFont(None, 60, bold=True)
            text1 = font1.render("GAME OVER", True, (255, 50, 50))
            text1_rect = text1.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
            self.screen.blit(text1, text1_rect)

            font2 = pygame.font.SysFont(None, 30)
            final = font2.render(f"Итоговый счёт: {self.snake.score}", True, (255, 255, 255))
            final_rect = final.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 10))
            self.screen.blit(final, final_rect)

            record_text = font2.render(f"Рекорд: {self.record}", True, (255, 215, 0))
            record_rect = record_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
            self.screen.blit(record_text, record_rect)

            restart = font2.render("Нажмите SPACE, чтобы начать заново", True, (200, 200, 100))
            restart_rect = restart.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 70))
            self.screen.blit(restart, restart_rect)

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)