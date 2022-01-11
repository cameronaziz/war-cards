from typing import List

import numpy as np


class Replay:
    def __init__(self, max_size: int, input_shape: List[int]):
        self.mem_size = max_size
        self.mem_cntr = 0
        self.input_shape = input_shape

        self.state_memory = np.zeros((self.mem_size, *input_shape), dtype=np.int32)
        self.new_state_memory = np.zeros((self.mem_size, *input_shape), dtype=np.int32)

        self.action_memory = np.zeros(self.mem_size, dtype=np.int32)
        self.reward_memory = np.zeros(self.mem_size, dtype=np.float32)
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.bool)

    # def setup(self):
    #     # if False:
    #         # if use_g_drive:
    #         saved = GDrive.read(settings_memory_location)
    #         if (
    #             saved == None
    #             or saved[0] != self.mem_size
    #             or saved[1] != self.input_shape
    #         ):
    #             self.write_settings()
    #             return
    #         self.mem_cntr = saved[2]
    #         state_memory = GDrive.read(state_memory_location)
    #         print(state_memory)
    #         action_memory = GDrive.read(action_memory_location)
    #         print(action_memory)
    #         reward_memory = GDrive.read(reward_memory_location)
    #         print(reward_memory)
    #         terminal_memory = GDrive.read(terminal_memory_location)
    #         print(terminal_memory)
    #         # if len(state_memory) > 0 \
    #         #     len(action_memory) > 0 and \
    #         #     len(reward_memory) > 0 and \
    #         #     len(terminal_memory) > 0:
    #         self.state_memory = state_memory
    #         self.action_memory = action_memory
    #         self.reward_memory = reward_memory
    #         self.terminal_memory = terminal_memory
    #         #   return
    #         # self.write_settings()

    # def write_settings(self):
    #     settings = (self.mem_size, self.input_shape, self.mem_cntr)
    #     GDrive.write(settings, settings_memory)

    def store_transition(
        self, state: List[int], state_: List[int], action: int, reward: int, done: bool
    ):
        index = self.mem_cntr % self.mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = state_
        self.action_memory[index] = action
        self.reward_memory[index] = reward
        self.terminal_memory[index] = done

        self.mem_cntr += 1
        # if self.mem_cntr % 50 == 0:
        #     self.g_drive_store()

    # def g_drive_store(self):
    #     if use_g_drive:
    #         GDrive.write(self.state_memory, state_memory)
    #         GDrive.write(self.action_memory, action_memory)
    #         GDrive.write(self.reward_memory, reward_memory)
    #         GDrive.write(self.terminal_memory, terminal_memory)
    #         self.write_settings()

    def sample_buffer(self, batch_size: int):
        max_mem = min(self.mem_cntr, self.mem_size)
        batch = np.random.choice(max_mem, batch_size, replace=False)

        states = self.state_memory[batch]
        states_ = self.new_state_memory[batch]
        actions = self.action_memory[batch]
        rewards = self.reward_memory[batch]
        dones = self.terminal_memory[batch]

        return states, actions, rewards, states_, dones
