import random
from typing import List

import numpy as np
import tensorflow as tf
from tensorflow.keras.optimizers import Adam

from ml.net import Net
from ml.replay import Replay


class Agent:
    def __init__(
        self,
        lr: float,
        gamma: float,
        n_actions: int,
        epsilon: float,
        batch_size: int,
        input_dims: List[int],
        epsilon_dec: float = 1e-6,
        eps_end: float = 0.01,
        mem_size: int = 1000000,
        fc1_dims: int = 32,
        fc2_dims: int = 32,
        replace: int = 100,
    ):
        self.n_actions = n_actions
        # self.action_space = [i for i in range(n_actions)]
        self.gamma = gamma
        self.epsilon = epsilon
        self.eps_dec = epsilon_dec
        self.eps_min = eps_end
        self.replace = replace
        self.batch_size = batch_size

        self.learn_step_counter = 0
        self.memory = Replay(mem_size, input_dims)
        self.q_eval = Net(n_actions, fc1_dims, fc2_dims)
        self.q_next = Net(n_actions, fc1_dims, fc2_dims)

        self.q_eval.compile(optimizer=Adam(learning_rate=lr), loss="mse")
        self.q_next.compile(optimizer=Adam(learning_rate=lr), loss="mse")

    def store(
        self,
        state: List[int],
        state_: List[int],
        action: int,
        reward: int,
        done: bool,
    ):
        self.memory.store_transition(state, state_, action, reward, done)

    def choose(self, observation: List[int]):
        if np.random.random() < self.epsilon:
            return random.randint(0, self.n_actions - 1)
        state = np.array([observation])
        actions = self.q_eval.advantage(state)
        result: int = tf.math.argmax(actions, axis=1).numpy()[0]
        return result

    def learn(self):
        if self.memory.mem_cntr < self.batch_size:
            return

        if self.learn_step_counter % self.replace == 0:
            self.q_next.set_weights(self.q_eval.get_weights())

        states, actions, rewards, states_, dones = self.memory.sample_buffer(
            self.batch_size
        )

        q_pred = self.q_eval(states)
        q_next = self.q_next(states_)
        q_target = q_pred.numpy()
        max_actions = tf.math.argmax(self.q_eval(states_), axis=1)
        for idx, _terminal in enumerate(dones):
            q_target[idx, actions[idx]] = rewards[idx] + self.gamma * q_next[
                idx, max_actions[idx]
            ] * (1 - int(dones[idx]))

        self.q_eval.train_on_batch(states, q_target)

        self.epsilon = (
            self.epsilon - self.eps_dec if self.epsilon > self.eps_min else self.eps_min
        )
        self.learn_step_counter += 1
