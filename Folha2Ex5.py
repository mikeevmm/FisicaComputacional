# -*- coding:utf-8 -*-

from types import FunctionType
from time import clock

def safe_newton (func : FunctionType, func_deriv : FunctionType,
                 a : float, b : float,
                 delta_x : float, delta_y : float,
                 max_steps : int, debug_info : dict = None):
    """
    Finds a zero in  [a, b].
    """
    if debug_info is not None:
        debug_info['iteration_count'] = 0
        debug_info['iterations'] = []

    x = (a+b)/2

    f_avg = f(x)
    delta = f_avg/f_prime(x)

    clock_start = clock()
    
    for _ in range(max_steps):
        if debug_info is not None:
            debug_info['iteration_count'] += 1
            debug_info['iterations'].append((x, f_avg))

        if abs(delta/f_avg) < delta_x or abs(f_avg) < delta_y:
            break

        delta = f_avg/f_prime(x)
        x = max(a, min(b, x - delta))
        f_avg = f(x)

    clock_end = clock()

    if debug_info is not None:
        debug_info['time'] = clock_end - clock_start

    return x

# Testing
if __name__ == '__main__':
    
    from math import log, sin, cos

# 1.
    f = lambda x: 25*x**4 - x**2/2 - 2
    f_prime = lambda x: 100*x**3 - x

    result = safe_newton(
        f,
        f_prime,
        0.2,
        1.2,
        1e-4,
        1e-4,
        10000
    )
    print(result)

# 2.
    f = lambda x: 2*cos(x)
    f_prime = lambda x: -2*sin(x)

    result = safe_newton(
        f,
        f_prime,
        0,
        10,
        1e-4,
        1e-4,
        10000
    )
    print(result)

# 3.
    f = lambda x: x**2 - 3 - sin(x)
    f_prime = lambda x: 2*x - cos(x)

    result = safe_newton(
        f,
        f_prime,
        0,
        10,
        1e-4,
        1e-4,
        10000
    )
    print(result)
# 4.
    g = lambda x: log(x) + 1/x**2 - 1
    g_prime = lambda x: 1/x - 2/x**3
# 4 b) iii. A)
    result = safe_newton(
        g,
        g_prime,
        1.4,
        2.4,
        1e-4,
        1e-4,
        10000
    )
    print(result)
# 4 b) iii. B)
    result = safe_newton(
        g,
        g_prime,
        1.4,
        2.4,
        1e-4,
        1e-4,
        10000
    )
    print(result)
# 4 c)
    result = safe_newton(
        g,
        g_prime,
        0.1,
        1.625,
        1e-4,
        1e-4,
        10000
    )

    print(result)