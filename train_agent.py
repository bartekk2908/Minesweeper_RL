from game import Game
from board import Board
from rl_agent import RL_Agent
from reward import *

from tqdm import tqdm
import pickle
import os

SAVE_MODEL_EVERY = 200   # save model and replay memory every _ games
DIR_NAME = "models"


def train_agent(board_size=(9, 9), num_bombs=10, visual_mode=True, number_of_games=100_000):
    if not os.path.exists(DIR_NAME):
        os.makedirs(DIR_NAME)

    board = Board(board_size, num_bombs)

    screen_size = (700, 700)
    env = Game(board, screen_size)
    if visual_mode:
        env.init_visualization()

    agent = RL_Agent(board_size, model_name="model_1")

    for i in tqdm(range(1, number_of_games+1, 1)):

        if visual_mode:
            env.agent_playing_visualization()

        current_state = board.represent_state()
        done = False
        while not done:

            action = agent.get_action(current_state)

            env.handle_click(action, True, False)

            new_state = board.represent_state()
            done = board.get_lost() or board.get_won()

            if visual_mode:
                env.agent_playing_visualization()

            reward = get_reward(action, current_state, new_state, num_bombs)

            agent.update_replay_memory(current_state, action, reward, new_state, done)
            agent.train(done)

            current_state = new_state.copy()

        board.reset()

        if not i % SAVE_MODEL_EVERY:

            # saving reply memory
            with open(f'{DIR_NAME}/{agent.model_name}.pkl', 'wb') as file:
                pickle.dump(agent.replay_memory, file)

            # saving model
            agent.model.save(f'{DIR_NAME}/{agent.model_name}.h5')


if __name__ == "__main__":
    train_agent(visual_mode=True)
