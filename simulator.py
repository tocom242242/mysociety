import copy
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from qlearning_agent import QLearningAgent
from grid_world import GridWorld

import pygame
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

FILED_TYPE = {
    "N": 0,  # 通常
    "G": 1,  # ゴール
    "W": 2,  # 壁
    "T": 3,  # トラップ
    "A": 4,  # トラップ
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


def draw_grid_world(grid):
    """
        grid world自体の再描画
    """
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            color = WHITE
            if grid[row][column] == FILED_TYPE["A"]:
                color = GREEN
            elif grid[row][column] == FILED_TYPE["G"]:
                color = RED
            elif grid[row][column] == FILED_TYPE["T"]:
                color = BLACK 
            elif grid[row][column] == FILED_TYPE["W"]:
                color = BLACK 
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
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Grid World")

    done = False

    clock = pygame.time.Clock()

   # grid worldの初期化
    grid_env = GridWorld() # grid worldの環境の初期化
    ini_state = grid_env.start_pos  # 初期状態（エージェントのスタート地点の位置）
    agent = QLearningAgent(epsilon=.1, actions=np.arange(4), observation=ini_state)  # Q学習エージェント

    nb_episode = 1000   #エピソード数
    rewards = []    # 評価用報酬の保存
    is_end_episode = False # エージェントがゴールしてるかどうか？

    step = 0
    # time.sleep(30)

    for episode in range(nb_episode):
        episode_reward = [] # 1エピソードの累積報酬
        while(is_end_episode == False):    # ゴールするまで続ける
            action = agent.act()  # 行動選択
            state, reward, is_end_episode = grid_env.step(action)
            agent.observe(state, reward)   # 状態と報酬の観測
            episode_reward.append(reward)

            screen.fill(BLACK)
            # grid worldの描画
            draw_grid_world(grid_env.map)
            # テキストを描画したSurfaceを作成
            step_str = sysfont.render("step:{}".format(step), False, WHITE)
            # 位# テキストを描画する
            screen.blit(step_str, (500,50))
            clock.tick(1)
            step += 1

            # 再描画
            pygame.display.flip()


        rewards.append(np.sum(episode_reward)) # このエピソードの平均報酬を与える
        state = grid_env.reset()    #  初期化
        agent.observe(state)    # エージェントを初期位置に
        is_end_episode = False

    # while not done:
    #     screen.fill(BLACK)
    #
    #     # grid worldの描画
    #     draw_grid_world()
    #
    #     # テキストを描画したSurfaceを作成
    #     step_str = sysfont.render("step:{}".format(step), False, WHITE)
    #     
    #     # 位# テキストを描画する
    #     screen.blit(step_str, (500,50))
    #
    #     clock.tick(1)
    #     step += 1
    #
    #     # 再描画
    #     pygame.display.flip()
    #
    #     # エージェントの位置の更新
    #     to_x, to_y = update_agent_pos(x, y)
    #
    #     grid[y][x] = 0
    #     grid[to_y][to_x] = 1
    #     x, y = to_x, to_y

    pygame.quit()