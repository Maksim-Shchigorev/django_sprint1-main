# ЗМЕЯЯЯЯЯЯЯЯЯ
import pygame
import random

# Инициализация pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Класс GameObject


class GameObject:
    def __init__(self, position):
        self.position = position

    def draw(self, surface):
        pass

# Класс Apple


class Apple(GameObject):
    def __init__(self, position):
        super().__init__(position)
        self.body_color = RED

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * CELL_SIZE,
                         random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE)

    def draw(self, surface):
        pygame.draw.circle(surface, self.body_color, (
            self.position[0] + CELL_SIZE // 2, self.position[1] + CELL_SIZE // 2), CELL_SIZE // 2)

# Класс Snake


class Snake(GameObject):
    def __init__(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = random.choice(
            [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        self.next_direction = None
        self.body_color = GREEN

    def update_direction(self, event):
        if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
            self.next_direction = event.key

    def move(self):
        cur_x, cur_y = self.positions[0]
        new_x, new_y = (cur_x, cur_y)

        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        if self.direction == pygame.K_UP:
            new_y -= CELL_SIZE
        elif self.direction == pygame.K_DOWN:
            new_y += CELL_SIZE
        elif self.direction == pygame.K_LEFT:
            new_x -= CELL_SIZE
        elif self.direction == pygame.K_RIGHT:
            new_x += CELL_SIZE

        self.positions = [(new_x, new_y)] + self.positions[:-1]

    def draw(self, surface):
        for pos in self.positions:
            pygame.draw.rect(surface, self.body_color,
                             (*pos, CELL_SIZE, CELL_SIZE))

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = random.choice(
            [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        self.next_direction = None

# Функция обработки событий клавиш


def handle_keys(event, snake):
    snake.update_direction(event)

# Основной цикл игры


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Game')

    snake = Snake()
    apple = Apple((random.randint(0, GRID_WIDTH - 1) * CELL_SIZE,
                  random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE))

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_keys(event, snake)

        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        screen.fill(BLACK)
        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()
        clock.tick(10)

    pygame.quit()


if __name__ == '__main__':
    main()
