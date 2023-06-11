from dqn import dqn
from random import random, choice, sample
import numpy as np
from collections import deque


class RL_Agent:
    def __init__(self, board_size, conv_units=64, dense_units=256, discount=0.1,
                 learn_rate=0.01, learn_decay=0.99975, learn_min=0.001,
                 epsilon=0.95, epsilon_decay=0.99975, epsilon_min=0.81,
                 memory_size=50_000, memory_min=1_000,
                 batch_size=64, update_target_every=5,
                 model=None):

        self.board_size = board_size

        self.learn_rate = learn_rate
        self.learn_decay = learn_decay
        self.learn_min = learn_min

        if model:   # if agent is being tested
            self.model = model
            self.epsilon = 0.0
        else:   # if agent is being trained
            self.model = dqn(self.learn_rate, self.board_size, self.board_size[0] * self.board_size[1], conv_units, dense_units)
            self.epsilon = epsilon
            self.epsilon_decay = epsilon_decay
            self.epsilon_min = epsilon_min

            self.discount = discount

            self.target_model = dqn(self.learn_rate, self.board_size, self.board_size[0] * self.board_size[1], conv_units, dense_units)
            self.target_model.set_weights(self.model.get_weights())

            self.replay_memory = deque(maxlen=memory_size)
            self.memory_min = memory_min

            self.batch_size = batch_size
            self.update_target_every = update_target_every
            self.target_update_counter = 0

            self.conv_units=conv_units
            self.dense_units=dense_units

    def get_action(self, state):
        possible_moves = []
        for row in range(self.board_size[0]):
            for col in range(self.board_size[1]):
                if state[row][col] == -1:
                    possible_moves.append((row, col))

        state = state.astype(np.int8) / 8
        state = state.astype(np.float16)

        rand = random()
        if rand < self.epsilon:     # random move (explore)
            action = choice(possible_moves)
        else:
            q_values = self.model.predict(np.reshape(state, (1, self.board_size[0], self.board_size[1], 1)), verbose=0)
            q_values = np.reshape(q_values, self.board_size)
            q_values[state != -0.125] = np.min(q_values)    # set already clicked tiles to min value
            action = np.unravel_index(np.argmax(q_values), self.board_size)

        return action

    def update_replay_memory(self, current_state, action, reward, new_state, done):
        current_state = current_state.astype(np.int8) / 8
        current_state = current_state.astype(np.float16)
        current_state = np.reshape(current_state, (self.board_size[0], self.board_size[1], 1))
        new_state = new_state.astype(np.int8) / 8
        new_state = new_state.astype(np.float16)
        new_state = np.reshape(new_state, (self.board_size[0], self.board_size[1], 1))

        self.replay_memory.append((current_state, action, reward, new_state, done))

    def train(self, current_done):
        if len(self.replay_memory) < self.memory_min:
            return

        batch = sample(self.replay_memory, self.batch_size)

        current_states = np.array([transition[0] for transition in batch])
        current_qs_list = self.model.predict(current_states, verbose=0)

        new_states = np.array([transition[3] for transition in batch])
        future_qs_list = self.target_model.predict(new_states, verbose=0)

        for i, (current_state, action, reward, new_state, done) in enumerate(batch):
            if not done:
                max_future_q = np.max(future_qs_list[i])
                new_q = reward + self.discount * max_future_q
            else:
                new_q = reward

            action = action[0] * self.board_size[1] + action[1]
            current_qs_list[i][action] = new_q

        self.model.fit(current_states, current_qs_list, batch_size=self.batch_size,
                       shuffle=False, verbose=0)

        # updating to determine if we want to update target_model yet
        if current_done:
            self.target_update_counter += 1

        if self.target_update_counter >= self.update_target_every:
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0

        # decay epsilon
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def get_params(self):
        return (self.board_size, self.learn_rate, self.learn_decay, self.learn_min, self.epsilon, self.epsilon_decay, self.epsilon_min,
                self.discount, self.replay_memory, self.memory_min, self.batch_size, self.update_target_every, self.target_update_counter,
                self.conv_units, self.dense_units)

    def load_params(self, params, model):
        (self.board_size, self.learn_rate, self.learn_decay, self.learn_min, self.epsilon, self.epsilon_decay, self.epsilon_min,
        self.discount, self.replay_memory, self.memory_min, self.batch_size, self.update_target_every, self.target_update_counter,
         self.conv_units, self.dense_units) = params
        self.model = model
        self.target_model = dqn(self.learn_rate, self.board_size, self.board_size[0] * self.board_size[1], self.conv_units, self.dense_units)
        self.target_model.set_weights(self.model.get_weights())
