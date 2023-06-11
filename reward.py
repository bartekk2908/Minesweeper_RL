from numpy import sum as np_sum

rewards = {'win': 1, 'lose': -1, 'progress': 0.3, 'guess': -0.3, 'no_progress': -0.3}


def is_guess(state, index):
    if np_sum(state == -1) == state.size:
        return False
    for row in range(index[0] - 1, index[0] + 2):
        for col in range(index[1] - 1, index[1] + 2):
            out_of_bounds = row < 0 or row >= state.shape[0] or col < 0 or col >= state.shape[1]
            same = row == index[0] and col == index[1]
            if same or out_of_bounds:
                continue
            if state[row][col] != -1:
                return False
    return True


def get_reward(index, old_state, new_state, num_bombs):
    if new_state[index] == -2:
        return rewards['lose']
    elif np_sum(new_state == -1) == num_bombs:
        return rewards['win']
    elif old_state[index] == new_state[index]:
        return rewards['no_progress']
    else:
        if is_guess(old_state, index):
            return rewards['guess']
        else:
            return rewards['progress']
