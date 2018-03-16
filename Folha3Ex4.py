# -*- coding:utf-8 -*-

from types import FunctionType

def dx_three (f : FunctionType, x : float, epsilon : float = 0.0001) -> float:
    return (f(x+epsilon) - f(x-epsilon))/(2*epsilon)

def ddx_three (f : FunctionType, x : float, epsilon : float = 0.0001) -> float:
    return (f(x+epsilon) - 2*f(x) + f(x-epsilon))/(epsilon*epsilon)

def dx_five (f : FunctionType, x : float, epsilon : float = 0.00001) -> float:
    return (f(x-2*epsilon) - 8*f(x-epsilon) + 8*f(x+epsilon) - f(x+2*epsilon))/(12*epsilon)

def ddx_five (f : FunctionType, x : float, epsilon : float = 0.0001) -> float:
    return (-f(x-2*epsilon) + 16*f(x-epsilon) - 30*f(x) + 16*f(x+epsilon) - f(x+2*epsilon))/(12*epsilon*epsilon)

# Testing
if __name__ == '__main__':
    from math import exp
    from decimal import Decimal
    import numpy as np
    import matplotlib.pyplot as plt

    FROM = 0
    TO = 12
    SAMPLE_RATE = 0.5

    for n in np.arange(0, 5, 0.5):
        
        xrange = np.arange(FROM,TO,SAMPLE_RATE/10**n)
        samples = len(xrange)
        funcvalue = np.empty(samples)
        dx_three_value = np.empty(samples)
        ddx_three_value = np.empty(samples)
        dx_five_value = np.empty(samples)
        ddx_five_value = np.empty(samples)

        difference = np.empty(samples)
        
        for i in range(samples):
            x = FROM + SAMPLE_RATE*i/10**(n)
            funcvalue[i] = exp(x)
            dx_three_value[i] = dx_three(exp, x, SAMPLE_RATE/10**n)
            ddx_three_value[i] = ddx_three(exp, x, SAMPLE_RATE/10**n)
            dx_five_value[i] = dx_five(exp, x, SAMPLE_RATE/10**n)
            ddx_five_value[i] = ddx_five(exp, x, SAMPLE_RATE/10**n)

            difference[i] = (abs(funcvalue[i] - dx_three_value[i]) +\
abs(funcvalue[i] - ddx_three_value[i]) + abs(funcvalue[i] - dx_five_value[i]) +\
abs(funcvalue[i] - ddx_three_value[i]))*10

        plt.title("h ~ {0:.2E}".format(Decimal(SAMPLE_RATE/10**n)))
        plt.xlim(FROM, TO)
        plt.ylim(0, 100)

        plt.plot(xrange, funcvalue, label="f(x)")
        plt.plot(xrange, dx_three_value, label="f'(x)  (Three points)")
        plt.plot(xrange, ddx_three_value, label="f''(x)   (Five points)")
        plt.plot(xrange, dx_five_value, label="f'(x)   (Five points)")
        plt.plot(xrange, ddx_five_value, label="f''(x)   (Five points)")
        plt.plot(xrange, difference, label="Sum of errors (x10)")
        plt.legend(loc='best')
        plt.show()
    
    print("""
Verifica-se que para valores de h suficientemente pequenos, o erro começa a aumentar.
    """)

    methods = ('dx_three', 'ddx_three', 'dx_five', 'ddx_five')
    relative_err = [np.empty(14) for _ in range(len(methods))]
    xrange = np.arange(1,15,1)

    for k in range(1, 15):
        for method in range(len(methods)):
            relative_err[method][k - 1] = abs(globals()[methods[method]](exp, 10, 10**(-k)) - exp(10))/exp(10)*100

    for index in range(len(relative_err)):
        plt.plot(xrange, relative_err[index], 'o', label='Relative error of {} (%)'.format(methods[index]))
    plt.legend(loc='best')
    plt.show()