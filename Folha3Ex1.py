# -*- coding: utf-8 -*-

from types import FunctionType

def integrate_rectangle (f : FunctionType, a : float, b: float, N : int) -> float:
    a,b = min(a,b),max(a,b)
    h = (b-a)/N
    return h*sum(f(a + n*h + h/2) for n in range(N))

def integrate_trapezoid (f : FunctionType, a : float, b : float, N : int) -> float:
    a,b = min(a,b),max(a,b)
    h = (b-a)/N
    return h/2*(f(a) + 2 * sum(f(a + i*h) for i in range(1, N)) + f(b))

if __name__ == '__main__':
    from math import exp
    from random import random

    def print_header(header):
        print('\033[95m' + header + '\033[0m')

    def print_comment(comment):
        print('\033[94m' + comment + '\033[0m')

    print_header("Rectangle method")
    print_comment("Difference between exp(10)-exp(1) and integral of exp from 1 to 10")

    for N in range(5):
        print_comment("\tWith {} splits:".format(10**N))
        print('\t', exp(10) - exp(1) - integrate_rectangle(exp, 1, 10, 10**N))
    
    print_header("Trapezoid method")
    print_comment("Difference between exp(10)-exp(1) and integral of exp from 1 to 10")

    for N in range(5):
        print_comment("\tWith {} splits:".format(10**N))
        print('\t', exp(10) - exp(1) - integrate_trapezoid(exp, 1, 10, 10**N))