#!/usr/bin/python3
import random

import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------


def MontyHall(k, m, n, switch=True):
    '''
    run simulation of single run given k winning doors, m total doors,
    n doors revealed
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


def RunSimulation(num_simulations, K=1, M=3, N=1):
    '''
    runs simple Monte Carlo on num_simulations iterations of MonteHall. 
    Returns two lists of success rate over iters for switching & no switching
    '''
    switch_successes = 0
    switch_success_per = []
    for i in range(num_simulations):
        result = MontyHall(K, M, N)
        if result == 1:
            switch_successes += 1
        switch_success_per.append(switch_successes/(i+1))

    no_switch_successes = 0
    no_switch_success_per = []
    for j in range(num_simulations):
        result = MontyHall(K, M, N, switch=False)
        if result == 1:
            no_switch_successes += 1
        no_switch_success_per.append(no_switch_successes/(j+1))

    return switch_success_per, no_switch_success_per

# -----------------------------------------------------------------------------


def Plot(switch_list, no_switch_list):
    # generates line plot from lists of success percentages
    plt.plot(switch_list, label='Switch')
    plt.plot(no_switch_list, label='No switch')
    plt.xlabel('number iterations', fontsize=14)
    plt.ylabel('Win percent', fontsize=14)
    plt.legend(bbox_to_anchor=(1, 1))
    plt.show()

# -----------------------------------------------------------------------------


def CalculateStatistics(switch_list, no_switch_list):
    '''
    determines if is a good idea to switch or not by comparing average 
    success rates for switching vs. not switching
    '''
    assert len(switch_list) == len(no_switch_list)
    num_omit = 10  # remove first few noisy points for smoother calculations
    num_points = float(len(switch_list) - num_omit)

    avg_switch = sum(switch_list[num_omit:]) / num_points
    avg_noswitch = sum(no_switch_list[num_omit:]) / num_points

    # if good idea to switch, two avgs converge to same val
    converges = False
    threshold = 1
    if abs(avg_switch - avg_noswitch) <= 1:
        converges = True

    return avg_switch, avg_noswitch, converges


# -----------------------------------------------------------------------------
def MonteCarlo(K_range=(1, 100), M_range=(1, 100), N_range=(1, 100)):
    '''
    run MonteCarlo w/ varying K, M, & N ranges to see pattern for when switching makes sense
    '''
    return "Work in progress"
# -----------------------------------------------------------------------------


'''
switch, noswitch = RunSimulation(10000, 1, 3, 1)
Plot(switch, noswitch)
CalculateStatistics(switch, noswitch)
'''
