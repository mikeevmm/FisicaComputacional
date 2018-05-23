#!/usr/bin/env python

if __name__ == '__main__':
    from Folha11Ex1 import euler
    from math import exp
    import numpy as np
    import matplotlib.pyplot as plt

    diff_eqs = (
        lambda x, y: y*x**2 - y,)

    def analytic(x, y0): return y0*np.exp(x**3/3-x)
    initial_conditions = (0, 1)
    Dt = 2

    for h in (0.001, 0.0001):
        steps = int(Dt/h)
        x_range = tuple(h*step for step in range(steps+1))
        y_values = euler(h, Dt, initial_conditions, diff_eqs, False)
        plt.plot(x_range, y_values, label='Euler; h = %f' % h)

    x_range = np.linspace(0, 2, 100)
    y_values = analytic(x_range, 1)
    plt.plot(x_range, y_values, label='Analytical')

    plt.legend(loc='best')
    plt.show()

    print("""
    In the set interval, the numerical approximations and analytical
    solution are virtually indistinguishable.
    """)
    input('ENTER TO QUIT')
