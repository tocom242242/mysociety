import pygame
import numpy as np
import copy
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

WIDTH = 40
HEIGHT = 40

WINDOW_SIZE = [700, 500]

MARGIN = 5

# 行動の集合
ACTIONS = {
    "UP": 0,
    "DOWN": 1,
    "LEFT": 2,
    "RIGHT": 3,
    "STAY": 4
}

def reset_grid():
    grid = []
    for row in range(10):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(10):
            grid[row].append(0)  # Append a cell

    return grid


def is_in_grid(x, y):
    """
        x, yがグリッドワールド内かの確認
    """
    if y < len(grid) and y >= 0:
        if x < len(grid[0]) and x >= 0:
            return True
    return False


def update_agent_pos(x, y):
    """
        エージェントの位置の更新 
    """

    while True:
        to_y, to_x = y, x
        action = np.random.randint(6)
        if action == ACTIONS["UP"]:
            to_y += -1
        elif action == ACTIONS["DOWN"]:
            to_y += 1
        elif action == ACTIONS["LEFT"]:
            to_x += -1
        elif action == ACTIONS["RIGHT"]:
            to_x += 1

        if is_in_grid(to_y, to_x) is True:
            return to_x, to_y


def draw_grid_world():
    """
        grid world自体の再描画
    """
    for row in range(10):
        for column in range(10):
            color = WHITE
            if grid[row][column] == 1:
                color = GREEN
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])


if __name__ == '__main__':

    pygame.init()

    # フォントの作成
    sysfont = pygame.font.SysFont(None, 40)

    # gridの情報
    grid = []
    for row in range(10):
        grid.append([])
        for column in range(10):
            grid[row].append(0)

    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Grid World")

    done = False

    clock = pygame.time.Clock()

    # エージェントの初期位置
    x, y = 1, 5
    grid[y][x] = 1

    step = 0
    time.sleep(30)
    while not done:
        screen.fill(BLACK)

        # grid worldの描画
        draw_grid_world()

        # テキストを描画したSurfaceを作成
        step_str = sysfont.render("step:{}".format(step), False, WHITE)
        
        # 位# テキストを描画する
        screen.blit(step_str, (500,50))

        clock.tick(1)
        step += 1

        # 再描画
        pygame.display.flip()

        # エージェントの位置の更新
        to_x, to_y = update_agent_pos(x, y)

        grid[y][x] = 0
        grid[to_y][to_x] = 1
        x, y = to_x, to_y

    pygame.quit()
