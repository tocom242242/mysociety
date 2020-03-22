import copy
import numpy as np
import os
import pickle


class QLearningAgent:
    """
        Q学習
    """

    def __init__(
            self,
            id=0,
            alpha=.2,
            epsilon=.1,
            epsilon_decay_rate=.99,
            gamma=.99,
            actions=None,
            is_learn=True,
            observation=None):
        self.id = id
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay_rate = epsilon_decay_rate
        self.reward_history = []
        self.actions = actions
        self.state = str(observation)
        self.ini_state = str(observation)
        self.previous_state = None
        self.previous_action = None
        self.is_learn = True,
        self.q_values = self._init_q_values()

    def _init_q_values(self):
        """
           Q テーブルの初期化
        """
        q_values = {}
        q_values[self.state] = np.repeat(0.0, len(self.actions))
        return q_values

    def init_state(self):
        """
            状態の初期化
        """
        self.previous_state = copy.deepcopy(self.ini_state)
        self.state = copy.deepcopy(self.ini_state)
        return self.state

    def set_q_value(self, q_values):
        self.q_values = q_values

    def act(self):
        # ε-greedy選択
        if np.random.uniform() < self.epsilon:  # random行動
            action = np.random.randint(0, len(self.q_values[self.state]))
        else:   # greedy 行動
            action = np.argmax(self.q_values[self.state])

        self.previous_action = action
        self.epsilon = self.epsilon * self.epsilon_decay_rate
        if self.epsilon < 0.01:
            self.epsilon = 0.01
        return action

    def observe(self, next_state, reward=None):
        """
            次の状態と報酬の観測
        """
        next_state = str(next_state)
        if next_state not in self.q_values:  # 始めて訪れる状態であれば
            self.q_values[next_state] = np.repeat(0.0, len(self.actions))

        self.previous_state = copy.deepcopy(self.state)
        self.state = next_state

        if reward is not None and self.is_learn:
            self.reward_history.append(reward)
            self.learn(reward)

    def learn(self, reward):
        """
            Q値の更新
        """
        q = self.q_values[self.previous_state][self.previous_action]  # Q(s, a)
        max_q = max(self.q_values[self.state])  # max Q(s')
        # Q(s, a) = Q(s, a) + alpha*(r+gamma*maxQ(s')-Q(s, a))
        self.q_values[self.previous_state][self.previous_action] = q + \
            (self.alpha * (reward + (self.gamma * max_q) - q))

    def save_data(self, base_dir):
        """データを保存する
        """
        filepath = os.path.join(
            base_dir, "{}_q_values.pickle".format(self.id))
        with open(filepath, mode="wb") as fo:
            pickle.dump(self.q_values, fo)
        # pickle.dump()
        # q_values = np.array(self.q_values)
        # np.save(filepath, q_values)
