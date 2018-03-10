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
    SAMPLE_RATE = 0.01

    for n in range(1,10):
        
        samples = int((TO - FROM)/SAMPLE_RATE*10**n)
        xrange = np.arange(FROM,TO,SAMPLE_RATE/10**n)
        funcvalue = np.empty(samples)
        dx_three_value = np.empty(samples)
        ddx_three_value = np.empty(samples)
        dx_five_value = np.empty(samples)
        ddx_five_value = np.empty(samples)
        
        for i in range(samples):
            x = FROM + SAMPLE_RATE*i/10**n
            funcvalue[i] = exp(x)
            dx_three_value[i] = dx_three(exp, x, SAMPLE_RATE/10**n)
            ddx_three_value[i] = ddx_three(exp, x, SAMPLE_RATE/10**n)
            dx_five_value[i] = dx_five(exp, x, SAMPLE_RATE/10**n)
            ddx_five_value[i] = ddx_five(exp, x, SAMPLE_RATE/10**n)
        
        plt.title("h ~ {0:.2E}".format(Decimal(SAMPLE_RATE/10**n)))
        plt.xlim(FROM, TO)
        plt.ylim(0, 100)

        plt.plot(xrange, funcvalue, label="f(x)")
        plt.plot(xrange, dx_three_value, label="f'(x)  (Three points)")
        plt.plot(xrange, ddx_three_value, label="f''(x)   (Five points)")
        plt.plot(xrange, dx_five_value, label="f'(x)   (Five points)")
        plt.plot(xrange, ddx_five_value, label="f''(x)   (Five points)")
        plt.legend(loc='best')
        plt.show()