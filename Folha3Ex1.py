# -*- coding: utf-8 -*-

from types import FunctionType

def rectangle_approximation_generator (f : FunctionType, a : float, b : float, N : int):
    a,b = min(a,b),max(a,b)
    h = (b-a)/N
    for i in range(N):
        sample = f(a+h*i)
        yield (a+h*(i - 0.5), sample)
        yield (a+h*(i + 0.5), sample)

def rectangle_generator (f : FunctionType, a : float, b: float, N : int):
    h = (b-a)/N
    for n in range(N):
        yield f(a + n*h + h/2)

def integrate_rectangle (f : FunctionType, a : float, b: float, N : int) -> float:
    a,b = min(a,b),max(a,b)
    h = (b-a)/N
    generator = rectangle_generator(f, a, b, N)
    return h*sum(generator)

def trapezoid_approximation_generator (f : FunctionType, a : float, b : float, N : int):
    a,b = min(a,b),max(a,b)
    h = (b-a)/N
    for i in range(N):
        yield (h*(i-0.5), f(a + h*(i - 0.5)))
        yield (h*(i+0.5), f(a + h*(i + 0.5)))

def trapezoid_generator (f : FunctionType, a : float, b : float, N : int):
    h = (b-a)/N
    yield f(a)
    for i in range(1, N):
        yield 2*f(a + i*h)
    yield f(b)

def integrate_trapezoid (f : FunctionType, a : float, b : float, N : int) -> float:
    a,b = min(a,b),max(a,b)
    h = (b-a)/N
    generator = trapezoid_generator(f,a,b,N)
    return h/2*sum(generator)

def simpson_approximation_generator (f : FunctionType, a : float, b : float, N : int):
    a,b = min(a,b),max(a,b)
    h = (b-a)/N
    P = 10
    for i in range(1, N+1, 2):
        x = a+i*h
        
        x1, y1 = x-h, f(x-h)
        x2, y2 = x, f(x)
        x3, y3 = x+h, f(x+h)
        A = (x3*(y2-y1)+x2*(y1-y3)+x1*(y3-y2))/((x1-x2)*(x1-x3)*(x2-x3))
        B = (x1**2*(y2-y3)+x3**2*(y1-y2)+x2**2*(y3-y1))/((x1-x2)*(x1-x3)*(x2-x3))
        C = (x2**2*(x3*y1-x1*y3)+x2*(x1**2*y3-x3**2*y1)+x1*x3*(x3-x1)*y2)/(((x1-x2)*(x1-x3)*(x2-x3)))

        for n in range(P):
            xx = x1 + (x3 - x1)/P*n
            yield (
                xx,
                A*xx**2 + B*xx + C
            )

def simpson_generator (f : FunctionType, a : float, b : float, N : int):
    h = (b-a)/N
    yield f(a)
    for i in range(1, N):
        yield (i%2*2+2)*f(a + h*i)
    yield f(b)

def integrate_simpson (f : FunctionType, a : float, b : float, N : int) -> float:
    a,b = min(a,b),max(a,b)
    h = (b-a)/N
    generator = simpson_generator(f, a, b, N)
    return h/3*sum(generator)

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np

    from types import GeneratorType
    from math import exp, cos, sin, pi, log
    from random import random

    def print_header(header):
        print('\033[95m' + header + '\033[0m')

    def print_comment(comment):
        print('\033[94m' + comment + '\033[0m')
    
    def wait():
        input("\033[1;93m Enter to continue...\033[0m")
        print("\033[1A\033[2K")
    
# ==== EX 1
    print_header("Ex. 1")
    print_comment("Integral 0 -> 0.5")
    
    f = lambda x: (10*exp(-x)*sin(2*pi*x))**2
    EXPECTED = 15.41260804810169
    RESOLUTION = 3

    for method in ('rectangle', 'trapezoid', 'simpson'):
        print_header("{} Method".format(method).title())
        
        integrator = globals()['integrate_' + method] # type: FunctionType

        i = 1
        result = integrator(f, 0, 0.5, i)
        while abs(result - EXPECTED) > 0.0001:
            i += 1
            result = integrator(f, 0, 0.5, i)

        print_comment("\tResult:")
        print('\t',result)
        print_comment("\tNeeded {} splits for error to go below 0.0001".format(i))

        generator = globals()[method + '_generator'](f, 0, 0.5, i) # type: GeneratorType
        touches = 0
        try:
            while True:
                next(generator)
                touches += 1
        except StopIteration:
            pass

        print_comment("\tAt this resolution, {} samples of the function were needed.".format(touches))
        
        print_header("Function approximation plot:")
        wait()

        approx_generator = globals()[method + '_approximation_generator']

        xvalues = np.array(list( map(lambda x: x[0], approx_generator(f, 0, 0.5, i) ) ))
        yvalues = np.array(list( map(lambda x: x[1], approx_generator(f, 0, 0.5, i) ) ))
        plt.plot(xvalues, yvalues)

        xoriginal = np.arange(0, 0.5, 1/(len(xvalues) * RESOLUTION))
        xsamples = len(xoriginal)
        yoriginal = np.empty(xsamples)
        for i in range(xsamples):
            yoriginal[i] = f(0.5/xsamples*i)
        plt.plot(xoriginal, yoriginal)
        
        plt.show()

# ===== EX 2
    print_header("Ex. 2")

    f = lambda x: 1/(1+x**2)

    print_comment("\t Numerical value for PI:")
    print(2*integrate_simpson(f, -1, 1, 10000))
    
    print_comment("\t Varying integration steps:")
    wait()

    STEPS = 200

    xvalues = np.empty(STEPS)
    yvalues = np.empty(STEPS)
    nice = None

    for i in range(1, STEPS + 1):
        xvalues[i - 1] = log(2/i)
        yvalues[i - 1] = integrate_simpson(f, -1, 1, i)
        if nice is None and abs(yvalues[i-1]*2 - pi) < 1E-6:
            nice = i
    
    plt.plot(xvalues, yvalues)
    plt.show()

    print_comment("\t At least {} splits were needed for a 1E-6 precision.".format(nice))
    print_comment("\t With only {}+1={} evaluations of the function we are able to calculate\
the value of the function with great precision.".format(nice, nice+1))