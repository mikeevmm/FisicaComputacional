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
            (0.00,   0.0       )  ,
            (0.25,   0.24740396)  ,        
            (0.50,   0.47942554)  ,        
            (0.75,   0.68163876)  ,        
            (1.00,   0.84147098)  ,        
            (1.25,   0.94898462)  ,        
            (1.50,   0.99749499)  ,        
            (pi/2,    1.0      )   
    )

    interpolation = get_lagrange_interpolate(data)

    xrange = np.linspace(0, pi/2)
    interpolation_y = tuple(
        interpolation(x) for x in xrange
    )

    def get_x (data):
        return tuple(map(lambda x: x[0], data))
    def get_y (data):
        return tuple(map(lambda x: x[1], data))

    plt.title("Data points and lagrange interpolation")
    plt.plot(get_x(data), get_y(data), 'o')
    plt.plot(xrange, interpolation_y)
    plt.show()

    plt.title("Lagrange interpolation vs Precise function")
    plt.plot(get_x(data), get_y(data), 'o', label='Data Points')
    plt.plot(xrange, interpolation_y, label='Interpolation')
    plt.plot(xrange, np.sin(xrange), label='Analytic function')
    plt.legend(loc='best')
    plt.show()

    error = np.abs(np.subtract(interpolation_y, np.sin(xrange)))
    
    print('''
We can see that the interpolation is very precise.
The maximum absolute error observable, at {}, is neglectable.
    '''.format(np.max(error)))