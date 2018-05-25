#!/usr/bin/env python

# -*- coding:utf-8 -*-

from random import randint, choice
from scipy.stats import chi2

def honest():
    return randint(1,6)

def loaded():
    return choice(tuple(range(1,6)) + (6,)*2)

def is_fair(func, throws):
    ONE_SIXTH = 1/6
    freq = [0]*6
    for _ in range(throws):
        side = func()
        freq[side - 1] += 1
    x2 = sum((freq[i] - ONE_SIXTH)**2/ONE_SIXTH for i in range(len(freq)))
    if x2 < chi2.isf(q = 0.05, df = 5):
        return True
    return False

if __name__ == '__main__':
    
    import matplotlib.pyplot as plt
    import numpy as np
    import threading

    THROWS = 1000
    RUNS = 10000
    TOTAL = THROWS*RUNS

    points = np.zeros((THROWS, 2))

    def run(throws):
        global points
        local = threading.local()
        local.fair_truths = 0
        local.loaded_truths = 0
        for _ in range(RUNS):
            if is_fair(honest, throws):
                local.fair_truths += 1
            if is_fair(loaded, throws):
                local.loaded_truths += 1
        points[throws,:] = (local.fair_truths/RUNS, local.loaded_truths/RUNS)

    threads = []
    for throws in range(THROWS):
        t = threading.Thread(target=run, args=(throws,))
        threads.append(t)
        t.start()
    
    for t in threads:
        print('Done')
        t.join()

    plt.plot(np.arange(THROWS), points, 'o')
    plt.show()        
