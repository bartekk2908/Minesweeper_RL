from game import Game
from board import Board
from rl_agent import RL_Agent
from reward import *


def train_agent(board_size=(9, 9), num_bombs=10, visual_mode=True, number_of_games=100):

    board = Board(board_size, num_bombs)

    if visual_mode:
        screen_size = (700, 700)
        env = Game(board, screen_size)
        env.init_visualization()
        env.visualize_agent()
        agent = RL_Agent(env)

        n_clicks = 0

        for i in range(1, number_of_games+1, 1):

            one_game_reward = 0

            current_state = board.represent_state()
            while not board.get_lost() and not board.get_won():
                # action = agent.get_action(current_state)
                action = (0, 0)
                env.handle_click(action, True, False)
                new_state = board.represent_state()

                env.visualize_agent()

                reward = get_reward(action, current_state, new_state, num_bombs)
                one_game_reward += reward

                # agent.update_replay_memory((current_state, action, reward, new_state, done))
                # agent.train(done)
                
                n_clicks += 1
                current_state = new_state.copy()

            board.reset_board()




    else:
        pass


if __name__ == "__main__":
    train_agent()
