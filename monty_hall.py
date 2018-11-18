#!/usr/bin/python3
import random

# -----------------------------------------------------------------------------


def MonteHall(k, m, n, switch=True):
    '''
    runs simulation of single Monte Hall run given k correct doors, m total doors, and n doors opened. User always switches when given option. Traditional Monte Hall would have l=1, m=3, n=1
    '''
    assert m - n - k >= 1

    doors = [0 for x in range(m)]
    prize_idx = random.sample(range(m), k)
    for idx in prize_idx:
        doors[idx] = 1

    goat_idx = [i for i in range(m) if doors[i] == 0]

    guess_idx = random.sample(range(m), 1)[0]

    print('doors: %s' % doors)
    print('goat idxs: %s' % goat_idx)
    print('guess idx: %s' % guess_idx)

    # something is wrong with switching logic
    if switch:
        # valid goat doors to reveal. List of all goats - guess door
        valid_goats_idx = list(set(goat_idx) - set([guess_idx]))

        valid = True
        while valid:
            rev_idx = random.sample(range(len(valid_goats_idx)), 1)[0]
            if rev_idx == guess_idx:
                valid = True
            else:
                valid = False

        guess_idx = list(set(doors) - set([doors[guess_idx]])
                         - set([doors[rev_idx]]))[0]

        print('valid goat idxs %s' % valid_goats_idx)
        print('final guess idx %s' % guess_idx)

    chosen_door = doors[guess_idx]
    if chosen_door != 1:
        print('Wrong choice!')
        return False
    else:
        print('Good choice!')
        return True

# -----------------------------------------------------------------------------


def RepeatSimulation(num_simulations):
    for i in range(num_simulations):
        simulate()

# -----------------------------------------------------------------------------


def Plot(switch_data, no_switch_data):
    # plots data for switching & no switching
    print('Hello world!')

# -----------------------------------------------------------------------------


MonteHall(1, 3, 1)
