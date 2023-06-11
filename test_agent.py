from game import Game
from board import Board
from rl_agent import RL_Agent

from tqdm import tqdm
from keras.models import load_model
from time import sleep


def test_agent(model_name, board_size, num_bombs, number_of_games=100_000, break_time=1.0, get_winrate_every=100, visual_mode=False):

    model = load_model(f'models/{model_name}.h5')

    board = Board(board_size, num_bombs)

    screen_size = (700, 700)
    env = Game(board, screen_size)
    if visual_mode:
        env.init_visualization()

    agent = RL_Agent(board_size, model_name=model_name, model=model)

    n_wins = 0

    for i in tqdm(range(1, number_of_games+1, 1)):

        if visual_mode:
            env.agent_playing_visualization()

        done = False
        while not done:

            current_state = board.represent_state()

            action = agent.get_action(current_state)

            env.handle_click(action, True, False)

            done = board.get_lost() or board.get_won()

            if visual_mode:
                env.agent_playing_visualization()

            if board.get_won():
                n_wins += 1

            if done:
                sleep(break_time * 2.0)
            else:
                sleep(break_time)

        board.reset()

        if not i % get_winrate_every:
            print(f"CURRENT WINRATE: {round(float(n_wins/i) * 100, 2)}%")


if __name__ == "__main__":
    test_agent("model_best", board_size=(9, 9), num_bombs=10, number_of_games=1000,
               break_time=0.0, get_winrate_every=10, visual_mode=True)