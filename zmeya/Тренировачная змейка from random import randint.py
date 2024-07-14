from random import randint

import pygame
import random
import sys

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject():
    def __init__(self, bg_color=None, fg_color=None):
        self.body_color = bg_color
        self.figure_color = fg_color
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def draw(self):
        pass


class Apple(GameObject):
    def __init__(self, bg_color=APPLE_COLOR, fg_color=None):
        super().__init__(bg_color=bg_color, fg_color=fg_color)
        self.randomize_position()

    def randomize_position(self):
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, width=1)


class Snake(GameObject):
    def __init__(self, bg_color=SNAKE_COLOR, fg_color=None):
        super().__init__(bg_color=bg_color, fg_color=fg_color)
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self):
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def move(self):
        head_x, head_y = self.positions[0]
        new_head = (
            head_x + self.direction[0] * GRID_SIZE, head_y + self.direction[1] * GRID_SIZE)
        self.positions.insert(0, new_head)

    def update_direction(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != DOWN:
                self.direction = UP
            elif event.key == pygame.K_DOWN and self.direction != UP:
                self.direction = DOWN
            elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                self.direction = LEFT
            elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                self.direction = RIGHT

    def grow(self):
        self.positions.append(self.positions[-1])

    def check_collision(self, apple):
        if self.positions[0] == apple.position:
            apple.randomize_position()
            self.grow()

    def reset(self):
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(event, snake):
    snake.update_direction(event)

# Основная логика игры.


def main():
    apple = Apple(bg_color=APPLE_COLOR)
    snake = Snake(bg_color=SNAKE_COLOR)

    while True:
        for event in pygame.event.get():
            handle_keys(event, snake)

        snake.move()
        snake.check_collision(apple)

        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


if __name__ == '__main__':
    main()
