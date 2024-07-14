from random import random, randint

import pygame as pg
import random

# Инициализация PyGame:
pg.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 640
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (196, 196, 196)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

ROTATION = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT
}

DIRECTIONS = {
    pg.K_UP: UP,
    pg.K_DOWN: DOWN,
    pg.K_LEFT: LEFT,
    pg.K_RIGHT: RIGHT
}

# Скорость движения змейки:
speed = 10
score = 0
record_score = 0
# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Настройка времени:
clock = pg.time.Clock()


class GameObject():
    """Класс GameObject является родительским классом"""

    def __init__(self, bg_color=BOARD_BACKGROUND_COLOR):
        """Инициалиция методов

        Args:
            bg_color (tuple, optional): цвет объекта, по умолчанию None.
            fg_color (tuple, optional): цвет рамки, по умолчанию None.

        """
        self.body_color = bg_color
        self.position = CENTER

    def draw(self):
        """Метод для pytest"""

    def draw_cell(self, position):
        """Метод для отрисовки объекта"""
        x, y = position
        rect = pg.Rect(x, y, GRID_SIZE, GRID_SIZE)
        pg.draw.rect(screen, self.body_color, rect)


class Apple(GameObject):
    """Класс Apple является дочерним классом GameObject"""

    def __init__(self, bg_color=APPLE_COLOR,
                 occupied_cells=set()):
        """Инициалиция методов

        Args:
            bg_color (tuple, optional): цвет яблока.
        """
        super().__init__(bg_color=bg_color)
        self.randomize_position(occupied_cells)

    def randomize_position(self, occupied_cells):
        """Метод для определения позиции"""
        while True:
            x = random.randint(0, GRID_WIDTH) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT) * GRID_SIZE
            if (x, y) not in occupied_cells:
                self.position = (x, y)
                break

    def draw(self):
        """Метод для отрисовки яблока"""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс Snake является дочерним классом GameObject"""

    def __init__(self, bg_color=SNAKE_COLOR, board_color=BOARD_BACKGROUND_COLOR):
        """Инициалиция методов

            Args:
                bg_color (tuple, optional): цвет змейки.
            """
        super().__init__(bg_color=bg_color)
        self.board_color = board_color
        self.reset()

    def draw(self, grow=False):
        """Отрисовка змейки"""
        dx, dy = self.direction
        head_x, head_y = self.get_head_position()
        new_head_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head_position = (new_head_x + dx * GRID_SIZE,
                             new_head_y + dy * GRID_SIZE)
        self.draw_cell(self.get_head_position())
        if grow:
            self.draw_cell(new_head_position)
        else:
            tail_position = self.positions.pop()
            pg.draw.rect(screen, self.board_color,
                         (tail_position[0], tail_position[1],
                          GRID_SIZE, GRID_SIZE))

    def move(self, grow=False):
        """Метод для движения змейки"""
        dx, dy = self.direction
        head_x, head_y = self.get_head_position()
        new_head = ((head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)

    def reset(self):
        """Сброс игры сначала"""
        self.positions = CENTER
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def get_head_position(self):
        """Определение позиции головы змейки

        Возвращает:
            self.positions[0] (tuple): Позиция головы.
        """
        return self.positions[0]

    def update_direction(self, new_direction=None):
        """Обновление направления движения"""
        if new_direction:
            self.direction = new_direction


def update_caption():
    """Обновление заголовка экрана"""
    pg.display.set_caption(
        f"Змейка, ESC-Выход, Скорость={speed}, Очки - {score}, "
        f"Рекорд- {record_score}, LSHIFT - ув.скор, LCtrl - ум.скор")


def handle_keys(snake, direction=None):
    """Управление клавишами"""
    global speed

    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RSHIFT:
                speed += 1
            elif event.key == pg.K_RCTRL:
                speed -= 1
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit
            else:
                new_direction = ROTATION.get((snake.direction, event.key))
                snake.update_direction(new_direction)

        elif event.type == pg.QUIT:
            pg.quit()
            raise SystemExit


def clear_board():
    """Очистка экрана"""
    screen.fill(BOARD_BACKGROUND_COLOR)


def main():
    """Основная логика игры"""
    snake = Snake()
    apple = Apple(occupied_cells=snake.positions)
    global record_score
    clear_board()

    while True:
        handle_keys(snake)
        snake.move()
        global score

        # Змея кусает яблоко
        if snake.get_head_position() == apple.position:
            apple.randomize_position(occupied_cells=snake.positions)
            snake.move(grow=True)
            score += 1
            if score > record_score:
                record_score = score

        # Змея кусает себя
        elif snake.get_head_position() in snake.positions[1:]:
            score = 0
            snake.reset()
            apple.randomize_position(occupied_cells=snake.positions)
            clear_board()

        apple.draw()
        snake.draw()
        update_caption()
        pg.display.update()
        clock.tick(speed)


if __name__ == '__main__':
    main()
