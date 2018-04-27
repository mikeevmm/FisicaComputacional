# -*- coding:utf-8 -*-

import numpy as np
# Please include Folha9Ex1.py in the same folder!
from Folha9Ex1 import min_sqrs

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    # Parse data
    with open('valores.dat') as file_io:
        pairs = tuple(map(lambda x: x.split(' '), filter(None, file_io.read().split('\n'))))
    x,y = tuple(map(lambda u: float(u[0]), pairs)), tuple(map(lambda u: float(u[1]), pairs))
    x,y = np.array(x), np.array(y)

    # Plot
    x_plt = np.linspace(x[0] - 1, x[-1] + 1, 100)
    for deg in range(1, 8):
        coefs = min_sqrs(x, y, deg)
        f = lambda x: sum(coefs[u]*x**u for u in range(len(coefs)))

        y_plt = f(x_plt)
        
        plt.plot(x_plt, y_plt, label='{} deg. polynomial'.format(deg))
    plt.legend(loc='best')
    plt.plot(x, y, 'o')
    plt.show()


    # Assymptotic behaviour
    plt.ylim(np.min(y) - 20, np.max(y) + 20)
    plt.xlim(x[0] - 10, x[-1] + 10)
    x_plt = np.linspace(x[0] - 10, x[-1] + 10, 100)
    for deg in range(1, 8):
        coefs = min_sqrs(x, y, deg)
        f = lambda x: sum(coefs[u]*x**u for u in range(len(coefs)))

        y_plt = f(x_plt)
        
        plt.plot(x_plt, y_plt, label='{} deg. polynomial'.format(deg))
    plt.legend(loc='best')
    plt.plot(x, y, 'o')
    plt.show()

print('''
The curvature of the points seem to indicate
that the function should be an even function.

On the other hand, the interpolation behaviour
of the tested functions (i.e. behaviour for x
where there are no points) is consistent with this,
and seems to confirm a second degree polynomial
fits this data best.
''')