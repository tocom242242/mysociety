"""動画用
"""

import pygame
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from qlearning_agent import QLearningAgent
from grid_world import GridWorld

import time
import pickle

import os

# os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.display.set_mode((640, 480))


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


def draw_grid_world(grid, screen):
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


def save_result(agents, episode, result_dir):
    # ディレクトリの作成
    result_path = os.path.join(
        result_dir, "{}".format(episode))
    os.mkdir(result_path)
    for agent in agents:
        agent.save_data(base_dir=result_path)


def main(cfg):
    pygame.init()

    # フォントの作成
    sysfont = pygame.font.SysFont(None, 40)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Grid World")

    done = False

    clock = pygame.time.Clock()

    # grid worldの初期化
    grid_env = GridWorld()  # grid worldの環境の初期化
    ini_state = grid_env.start_pos  # 初期状態（エージェントのスタート地点の位置）
    agent = QLearningAgent(
        epsilon=cfg["agent"]["epsilon"],
        epsilon_decay_rate=cfg["agent"]["epsilon_decay_rate"],
        actions=np.arange(4),
        observation=ini_state,
        is_learn=False)  # Q学習エージェント

    nb_episode = cfg["nb_episode"]  # エピソード数
    save_interval = cfg["save_interval"]
    result_dir = cfg["result_dir"]
    max_step = 5
    rewards = []    # 評価用報酬の保存
    is_end_episode = False  # エージェントがゴールしてるかどうか？

    step = 0
    # time.sleep(30)

    for episode in range(nb_episode):
        print(episode)
        if episode % save_interval == 0:
            filepath = os.path.join(
                cfg["result_dir"],
                "{}/0_q_values.pickle".format(episode))
            with open(filepath, mode='rb') as fi:
                q_values = pickle.load(fi)
            agent.set_q_value(q_values)
            print("episode:", episode)
            episode_reward = []  # 1エピソードの累積報酬
            step = 0
            while(is_end_episode is False and step < max_step):    # ゴールするまで続ける
                action = agent.act()  # 行動選択
                state, reward, is_end_episode = grid_env.step(action)
                agent.observe(state, reward)   # 状態と報酬の観測
                episode_reward.append(reward)

                screen.fill(BLACK)
                # grid worldの描画
                draw_grid_world(grid_env.map, screen)
                # テキストを描画したSurfaceを作成
                episode_str = sysfont.render(
                    "episode:{}".format(episode), False, WHITE)
                step_str = sysfont.render("step:{}".format(step), False, WHITE)
                # 位# テキストを描画する
                screen.blit(episode_str, (500, 30))
                screen.blit(step_str, (500, 70))
                clock.tick(1)
                step += 1

                # 再描画
                pygame.display.flip()

            rewards.append(np.sum(episode_reward))  # このエピソードの平均報酬を与える
            state = grid_env.reset()  # 初期化
            agent.observe(state)    # エージェントを初期位置に
            is_end_episode = False
            print("step:", step)

    pygame.quit()


if __name__ == "__main__":
    config = {
        "nb_episode": 10,
        "nb_agents": 3,
        "save_interval": 2,
        "result_dir": "./result/",
        "agent": {"epsilon": .01,
                  "epsilon_decay_rate": 1.,
                  }
    }
    main(config)
