#!/usr/bin/python3
import sys
import random
import argparse

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
    runs simple Monte Carlo on num_simulations iterations of MontyHall. 
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


def CalculateConvergence(switch_list, no_switch_list):
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
    threshold = 0.5
    if abs(avg_switch - avg_noswitch)*100 <= threshold:
        converges = True

    return avg_switch, avg_noswitch, converges

# -----------------------------------------------------------------------------


def MonteCarlo(n_iter, K_max=10, M_max=10, N_max=10):
    '''
    [-m] optional arg

    run MonteCarlo w/ varying K, M, & N ranges. Returns lists of all settings 
    tested and all convergent configurations
    '''
    count = 0
    tested_settings = {}
    conv_settings = []
    while count < n_iter:
        # choose random config that's legal
        K = random.randint(1, K_max)
        M = random.randint(1, M_max)
        N = random.randint(1, N_max)

        # prevents tested duplicate settings
        if (K, M, N) in list(tested_settings.keys()):
            break

        if M - N - K >= 1:
            # run simulation of random config. Saves all results and
            # all convergent configs
            switch, no_switch = RunSimulation(100, K, M, N)
            switch_avg, no_switch_avg, conv = CalculateConvergence(
                switch, no_switch)

            tested_settings[(K, M, N)] = [switch_avg, no_switch_avg]

            if conv and (K, M, N) not in conv_settings:
                conv_settings.append((K, M, N))
            count += 1

    return tested_settings, conv_settings

# -----------------------------------------------------------------------------


def GeneratePlot(switch_list, no_switch_list):
    '''
    [-p] optional arg

    generates line plot from lists of success percentages. Used to visualize 
    convergence of one configuration i.e one (K, M, N) setting. 
    '''
    plt.plot(switch_list, label='Switch')
    plt.plot(no_switch_list, label='No switch')
    plt.xlabel('number iterations', fontsize=14)
    plt.ylabel('Win percent', fontsize=14)
    plt.legend(bbox_to_anchor=(1, 1))
    plt.show()

# -----------------------------------------------------------------------------


def PlotMonteCarlo(conv_results):
    '''
    Take in list of settings that converged and generate plot
    '''
    conv_switch_list = []
    conv_noswitch_list = []
    for config in conv_results:
        conv_switch, conv_noswitch = RunSimulation(
            100, config[0], config[1], config[2])
        conv_switch_list.append(conv_switch)
        conv_noswitch_list.append(conv_noswitch)

    for switch_stats in conv_switch_list:
        for noswitch_stats in conv_noswitch_list:
            plt.plot(switch_stats, label='Switch')
            #plt.plot(noswitch_stats, label='No switch')

    plt.xlabel('number iterations', fontsize=14)
    plt.ylabel('Win percent', fontsize=14)
    plt.legend(bbox_to_anchor=(1, 1))
    plt.show()

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    '''
    Usage: ./monty_hall.py [n winning doors] [n total doors] [n revealed doors]

    Optional args: [-m run Monte Carlo simulations] [-p Generate plot]
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('K', help='number winning doors', type=int)
    parser.add_argument('M', help='number total doors', type=int)
    parser.add_argument('N', help='number doors revealed', type=int)
    parser.add_argument('n_iter', help='number iterations to run', type=int)

    parser.add_argument('-m', '--monte_carlo',
                        help='run monte carlo. Prints out list of convergences',
                        action='store_true')
    parser.add_argument('-p', '--plot',
                        help='Generates plot of success vs. n_iter',
                        action='store_true')

    args = parser.parse_args()

    if args.monte_carlo:
        no_conv, conv_list = MonteCarlo(args.n_iter, args.K, args.M, args.N)
        print('Convergent (K,M,N) configurations:')
        for config in conv_list:
            print(config)
        print('Total convergent configs: %s' % len(conv_list))
    else:
        switch, noswitch = RunSimulation(args.n_iter, args.K, args.M, args.N)
        avg_switch, avg_noswitch, conv = CalculateConvergence(switch, noswitch)
        print('Switch win percent: %s' % avg_switch)
        print('No switch win percent: %s' % avg_noswitch)
        print('Converges?:  %s' % conv)
        if args.plot:
            GeneratePlot(switch, noswitch)
