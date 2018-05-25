#!/usr/bin/env python

# -*- coding:utf-8 -*-

from random import randint, choice
from scipy.stats import chi2

XI2C = chi2.isf(q=0.05, df=5)


def honest():
    return randint(1, 6)


def loaded():
    return choice(tuple(range(1, 6)) + (6,)*2)


def is_fair(func, throws):
    freq = [0]*6
    for _ in range(throws):
        side = func()
        freq[side - 1] += 1
    x2 = sum((freq[i] - throws/6)**2*6/throws for i in range(len(freq)))
    if x2 < XI2C:
        return True
    return False


if __name__ == '__main__':

    import matplotlib.pyplot as plt
    import numpy as np
    import concurrent.futures
    from time import sleep

    THROWS = 1000
    THROW_STEP = 20
    RUNS = 100

    point_range = np.arange(THROW_STEP, THROWS, THROW_STEP)
    points = np.zeros((len(point_range), 2))

    def run(throws):
        global points
        fair_truths = 0
        loaded_truths = 0
        for _ in range(RUNS):
            if is_fair(honest, throws):
                fair_truths += 1
            if is_fair(loaded, throws):
                loaded_truths += 1
        points[int(throws/THROW_STEP) - 1, :] = (fair_truths /
                                             RUNS, loaded_truths/RUNS)

    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        for throws in point_range:
            executor.submit(run, throws)

    plt.title('~Probability of fairness for N throws')
    plt.xlabel('N. of throws')
    plt.plot(point_range, points[:,0], 'o', label='Fair die')
    plt.plot(point_range, points[:,1], 'o', label='Loaded die')
    plt.legend(loc='center right')
    plt.show()
