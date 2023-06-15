from game import Game
from board import Board
from rl_agent import RL_Agent

from tqdm import tqdm
from keras.models import load_model
from time import sleep
import os
from pygame import image
import shutil


SCREENS_DIR = "screenshots"

def test_agent(model_name, board_size=(9, 9), num_bombs=10, number_of_games=100_000, break_time=0.0, get_winrate_every=100,
               visual_mode=False, saving_frames=False):

    if os.path.exists(SCREENS_DIR):
        shutil.rmtree(SCREENS_DIR)
    os.makedirs(SCREENS_DIR)

    model = load_model(f'models/{model_name}.h5')

    board = Board(board_size, num_bombs)

    screen_size = (700, 700)
    env = Game(board, screen_size)
    if visual_mode:
        env.init_visualization()

    agent = RL_Agent(board_size, model=model)

    n_wins = 0
    progress = 0
    max_progress = board_size[0] * board_size[1] - num_bombs

    for i in tqdm(range(1, number_of_games+1, 1)):

        j = 0   # number of move in one game

        if visual_mode:
            env.agent_playing_visualization()
            if saving_frames:
                os.makedirs(f"{SCREENS_DIR}\\{i}")
                image.save(env.screen, f"{SCREENS_DIR}\\{i}\\{j}.jpg")

        done = False
        while not done:

            j += 1

            current_state = board.represent_state()

            action = agent.get_action(current_state)

            env.handle_click(action, True, False)

            done = board.get_lost() or board.get_won()

            if visual_mode:
                env.agent_playing_visualization()
                if saving_frames:
                    image.save(env.screen, f"{SCREENS_DIR}\\{i}\\{j}.jpg")

            if board.get_won():
                n_wins += 1

            if done:
                progress += board.get_num_clicked()
                sleep(break_time * 2.0)
            else:
                sleep(break_time)

        board.reset()

        if not i % get_winrate_every:
            print(f"CURRENT WINRATE: {round(float(n_wins/i) * 100, 2)}%\tAVERAGE PROGRESS: {round(float(progress/(i*max_progress)) * 100, 2)}%")


if __name__ == "__main__":
    test_agent("model_test_9x9_10", number_of_games=30, break_time=0.0, get_winrate_every=100, visual_mode=True, saving_frames=True)
