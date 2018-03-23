# -*- coding:utf-8 -*-

from itertools import chain
from functools import reduce

def prod (of):
    return reduce(lambda a,b: a*b, of)

def get_lagrange_interpolate (data):
    '''
    Returns a function corresponding
    to the Lagrange interpolation of given
    set of (x,y) data.
    '''
    def get_L (i):
        terms = chain(range(0,i), range(i+1, len(data))) # skip i
        return lambda x: prod( (x-data[k][0])/(data[i][0] - data[k][0]) for k in terms )

    return lambda x: sum(data[i][1] * get_L(i)(x) for i in range(len(data)))

if __name__ == '__main__':

    import matplotlib.pyplot as plt
    import numpy as np
    from math import pi

    data = (
        (1920,    106.46),
        (1930,    123.08),
        (1940,    132.12),
        (1950,    152.27),
        (1960,    180.67),
        (1970,    205.05),
        (1980,    227.23),
        (1990,    249.46),
        (2000,    281.42)
    )

    interpolation = get_lagrange_interpolate(data[:-1])

    xrange = np.arange(1900, 2010, 0.1)
    
    interpolation_y = tuple(
        interpolation(x) for x in xrange
    )
    plt.plot(xrange, interpolation_y, label='Lagrange interpolation.')
    plt.plot(tuple(x[0] for x in data), tuple(x[1] for x in data), 'o', label='Data (1920 - 1990)')
    plt.legend(loc='best')
    plt.show()

    print('''
Predicted population in 2000: {}

Actual population in 2000: {}
'''.format(interpolation(2000), data[-1]))

    print('''\
One can see that, while the interpolation is very good at including the
considered points, it is not adequate to extrapolate the data.

This is especially visible on the plot, where an approximately linear growth
is interpolated as an odd polynomial function.
    ''')