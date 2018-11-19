#!/usr/bin/python3
import random

# -----------------------------------------------------------------------------


def MonteHall(k, m, n, switch=True):
    '''
    run simulation of single run given k winning doors, m total doors,
    n total doors
    '''
    assert m - n - k >= 1
    # randomly choose winning door
    door_idx = list(range(m))
    doors = [0 for x in range(m)]
    prize_idx = random.sample(range(m), k)

    for idx in prize_idx:
        doors[idx] = 1
        guess = random.choice(door_idx)

        if switch:
            # generate all goat doors - guessed door, choose one to reveal
            remain_door_idx = list(
                set(door_idx) - set([guess]) - set(prize_idx))
            rev_door = random.choice(remain_door_idx)
            # new guess after switching doors
            guess = list(set(door_idx) - set([guess]) - set([rev_door]))[0]

        if doors[guess] != 0:
            return 1
        else:
            return 0

# -----------------------------------------------------------------------------


def MonteCarlo(num_simulations, K=1, M=3, N=1):
    switch_successes = 0
    switch_fails = 0
    for i in range(num_simulations):
        result = MonteHall(K, M, N)
        if result == 1:
            switch_successes += 1
        else:
            switch_fails += 1

    no_switch_successes = 0
    no_switch_fails = 0
    for i in range(num_simulations):
        result = MonteHall(K, M, N, switch=False)
        if result == 1:
            no_switch_successes += 1
        else:
            no_switch_fails += 1

    print('Switch percent wins: %s' % (switch_successes/num_simulations))
    print('Switch percent loss: %s' % (switch_fails/num_simulations))
    print('No switch percent wins: %s' % (no_switch_successes/num_simulations))
    print('No switch percent loss: %s' % (no_switch_fails/num_simulations))

# -----------------------------------------------------------------------------


def Plot(switch_data, no_switch_data):
    # plots data for switching & no switching
    print('Hello world!')

# -----------------------------------------------------------------------------


# MonteCarlo(10000)
