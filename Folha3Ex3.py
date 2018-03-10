# -*- coding:utf-8 -*-

from types import FunctionType
from random import uniform,random

def monte_carlo (f : FunctionType, a : float, b : float, fmax : float, precision : int):
    a,b=min(a,b),max(a,b)
    inside = 0
    for _ in range(precision):
        xy = (uniform(a,b), uniform(0, fmax))
        if xy[1] < f(xy[0]):
            inside += 1
    return inside/precision*((b-a)*fmax)

if __name__ == '__main__':

    from math import pi

    def print_header(header):
        print('\033[95m' + header + '\033[0m')

    def print_comment(comment):
        print('\033[94m' + comment + '\033[0m')
    
    def wait():
        input("\033[1;93m Enter to continue...\033[0m")
        print("\033[1A\033[2K")
    
    f = lambda x: 1/(1+x**2)

    nice = 1
    while True:
        result = 2*monte_carlo(f, -1, 1, 1.1, nice)
        if abs(result - pi) < 1E-6:
            break
        nice += 1

    print_comment("At {} random throws, the error on pi is smaller than 1E-6.".format(nice))
    print_comment("This is much less effective than all previously tested algorithms.")