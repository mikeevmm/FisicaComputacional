# -*- coding:utf-8 -*-

from types import FunctionType
from time import clock

def bissection (f : FunctionType, a : float, b : float, x_delta : float, y_delta : float, max_steps : int, debug_info : dict = None):
    """
    Find a zero of `f`, using the bissection method,
    in the ]a, b[ interval,
    with `x_delta` precision on |x_a = x_b|,
    `y_delta` precision on |f(x) = 0|,
    and max `max_steps` iterations.
    
    (Setting debug_info makes this function slower!)
    """

    if f(a) * f(b) > 0:
        raise Exception("Cannot apply bissection method if a,b such that f(a)*f(b) > 0!")
    
    if debug_info is not None:
        debug_info['iteration_count'] = 0
        debug_info['iterations'] = []

    f_a = f(a)
    f_b = f(b)

    clock_start = clock()

    for _ in range(max_steps):
        if debug_info is not None:
            debug_info['iteration_count'] += 1
            debug_info['iterations'].append(((a, f_a), (b, f_b)))

        delta = (b - a)/2
        x_avg = a + delta
        f_avg = f(x_avg)

        if delta/abs(x_avg) < x_delta or abs(f_avg) < y_delta:
            break

        if f_a * f_avg < 0:
            b = x_avg
            f_b = f_avg
        else:
            a = x_avg
            f_a = f_avg
    
    clock_end = clock()

    if debug_info is not None:
        debug_info['time'] = clock_end - clock_start

    return x_avg

def secant (f : FunctionType, a : float, b : float, x_delta : float, y_delta : float, max_steps : int, debug_info : dict = None):
    """
    Find a zero of `f`, using the secant method,
    in the ]a, b[ interval,
    with `x_delta` precision on |x_a = x_b|,
    `y_delta` precision on |f(x) = 0|,
    and max `max_steps` iterations.
    
    (Setting debug_info makes this function slower!)
    """

    f_a = f(a)
    f_b = f(b)

    if f_a * f_b > 0:
        raise Exception("Cannot apply secant method if a,b such that f(a)*f(b) > 0!")
    
    if debug_info is not None:
        debug_info['iteration_count'] = 0
        debug_info['iterations'] = []

    delta = f_a * (a - b)/(f_b - f_a)
    x_avg = a + delta
    f_avg = f(x_avg)

    clock_start = clock()

    for _ in range(max_steps):
        if debug_info is not None:
            debug_info['iteration_count'] += 1
            debug_info['iterations'].append(((a, f_a), (b, f_b)))

        if delta/abs(x_avg) < x_delta or abs(f_avg) < y_delta:
            break

        delta = f_a * (a - b)/(f_b - f_a)
        x_avg = a + delta
        f_avg = f(x_avg)

        if f_a * f_avg < 0:
            b = x_avg
            f_b = f_avg
        else:
            a = x_avg
            f_a = f_avg

    clock_end = clock()

    if debug_info is not None:
        debug_info['time'] = clock_end - clock_start

    return x_avg


def newton (f : FunctionType, f_prime : FunctionType, x : float, x_delta : float, y_delta : float, max_steps : int, debug_info : dict = None):
    """
    Find a zero of `f`, using Newton's method,
    starting from x,
    where `f_prime` is the first derivative of `f`,
    and with `x_delta` precision on |x_a = x_b|,
    `y_delta` precision on |f(x) = 0|,
    and max `max_steps` iterations.
    
    (Setting debug_info makes this function slower!)
    """

    if debug_info is not None:
        debug_info['iteration_count'] = 0
        debug_info['iterations'] = []

    f_avg = f(x)
    delta = f_avg/f_prime(x)

    clock_start = clock()
    
    for _ in range(max_steps):
        if debug_info is not None:
            debug_info['iteration_count'] += 1
            debug_info['iterations'].append((x, f_avg))

        if abs(delta/f_avg) < x_delta or abs(f_avg) < y_delta:
            break

        delta = f_avg/f_prime(x)
        x = x - delta
        f_avg = f(x)

    clock_end = clock()

    if debug_info is not None:
        debug_info['time'] = clock_end - clock_start

    return x        


# Testing
if __name__ == '__main__':

    import numpy as np
    from pprint import pprint
    from math import sin, cos, log
    from matplotlib import pyplot as plt

    def wait ():
        input("\033[1;93m Enter to continue...\033[0m")
        print("\033[1A\033[2K")
    
    def print_ex_label (i):
        print("\033[95m\n"+"@"*34+"\n@@\t\tEX. "+str(i)+"\t\t@@\n"+"@"*34+"\033[0m")

    def print_comment (comment):
        print("\033[92m" + comment + "\033[0m")

# ======  Ex. 1
    print_ex_label(1)

    bissec_debug = {}
    secant_debug = {}

    test_func = lambda x: 25*x**4-x**2/2-2

    bissec_result = bissection(test_func, 0.2, 1.2, 0.0001, 0.0001, 1000, bissec_debug)
    secant_result = secant(test_func, 0.2, 1.2, 0.0001, 0.0001, 1000, secant_debug)

    print("Bissection result: {}".format(bissec_result))
    print("Secant result: {}".format(secant_result))

    wait()

    print("Bissection debug data:")
    pprint(bissec_debug)

    print("Secant debug data:")
    pprint(secant_debug)

    wait()

# ======  Ex. 2
    print_ex_label(2)

    test_func = lambda x: 2*cos(x)
    test_func_deriv = lambda x: -2*sin(x)

    newton_debug = {}

    newton_result = newton(test_func, test_func_deriv, 7, 0.0001, 0.0001, 1000, newton_debug)

    print("Newton result: {}".format(newton_result))
    print("Newton debug data:")
    pprint(newton_debug)

    print_comment("""
Verifica-se que o método é bom para o caso, convergindo rapidamente (7 iterações)
e para um bom resultado (erro ~ 1e-7).
    """)

    wait()

    bissec_debug = {}
    secant_debug = {}
    newton_debug_1 = {}
    newton_debug_2 = {}

    bissec_result = bissection(test_func, 0, 10, 0.0001, 0.0001, 1000, bissec_debug)
    secant_result = secant(test_func, 0, 10, 0.0001, 0.0001, 1000, secant_debug)

    try:
        newton_result_1 = newton(test_func, test_func_deriv, 0, 0.0001, 0.0001, 1000, newton_debug_1)
    except ZeroDivisionError:
        newton_result_1 = 'O método diverge (divisão por 0)'
    
    try:
        newton_result_2 = newton(test_func, test_func_deriv, 10, 0.0001, 0.0001, 1000, newton_debug_2)
    except ZeroDivisionError:
        newton_result_2 = 'O método diverge (divisão por 0)'

    print("Bissection result: {}".format(bissec_result))
    print("Secant result: {}".format(secant_result))

    print_comment("Resultados consistentes com Newton partindo de x = 7.")
    wait()

    print("Newton result (x = 0): {}".format(newton_result_1))
    print("Newton result (x = 10): {}".format(newton_result_2))

    wait()

    print("Bissection debug data:")
    pprint(bissec_debug)

    print("Secant debug data:")
    pprint(secant_debug)

    #print("Newton debug data (x=0):")
    #pprint(newton_debug_1)

    print("Newton debug data (x=10):")
    pprint(newton_debug_2)

    wait()

    print_comment("""
Uma vez que a função possui multiplos zeros relativamente próximos,
verifica-se que apesar da bissecção e secante convergirem para
o mesmo zero, o método de Newton partindo de (x=10) converge, mas para
um zero diferente.

Por outro lado, o método de Newton diverge quando x inicial é 0, o que é
esperado, uma vez que a derivada na função é nula nesse ponto.
    """)

    wait()

# ======  Ex.3
    print_ex_label(3)

    test_func = lambda x: x**2 - 3 - sin(x)
    test_func_deriv = lambda x: 2*x - cos(x)

    bissec_debug = {}
    newton_debug = {}

    bissec_result = bissection(test_func, 0, 10, 0.0001, 0.0001, 10000, bissec_debug)
    newton_result = newton(test_func, test_func_deriv, 10, 0.0001, 0.0001, 10000, newton_debug)

    print("Bissection result: {}".format(bissec_result))
    print("Newton result: {}".format(newton_result))

    wait()

    print("Bissection debug data:")
    pprint(bissec_debug)
    print("Newton debug data:")
    pprint(newton_debug)

    wait()

    print_comment("""
Verifica-se que o método de Newton converge muito mais rapidamente,
e para o mesmo resultado que obtido por bissecção.
    """)

    wait()

# ======  Ex.4 a)
    print_ex_label('4a)')

    test_func = lambda x: log(x) + 1/x**2 - 1
    test_func_deriv = lambda x: 1/x - 2/x**3

    x_range = np.arange(0.1, 3.1, 0.01)
    func_vals = tuple(test_func(x) for x in x_range)
    plt.plot(x_range, func_vals)
    plt.axhline(y=0, color='k')
    plt.xlim((0.5, 3))
    plt.ylim((-1.1, 1.1))
    plt.show()

    print_comment("""
A função tem dois zeros.

O primeiro encontra-se no intervalo [0.75 : 1.75].

O segundo zero encontra-se no intervalo [2.0 : 2.5]
    """)

    wait()

# ======  Ex. 4 b)
    print_ex_label("4b)")
    
# ======  4 b) i)
    print("\033[35m i) \033[0m")

    bissec_debug = {}
    bissec_result = bissection(test_func, 1.4, 2.4, 0.0001, 0.0001, 1000, bissec_debug)

    print("Bissection result: {}".format(bissec_result))
    wait()
    print("Bissection debug data:")
    pprint(bissec_debug)
    wait()

# ======  4 b) ii)
    print("\033[35m ii) \033[0m")

    secant_debug = {}
    secant_result = secant(test_func, 1.4, 2.4, 0.0001, 0.0001, 1000, secant_debug)
    
    print("Secant result: {}".format(secant_result))
    wait()
    print("Secant debug data:")
    pprint(secant_debug)
    wait()

    print_comment("Consistente com o resultado obtido previamente. (mais eficaz)")
    wait()

# ======  4 b) iii) a)
    print("\033[35m ii) \033[0m")
    print("\033[31m A) \033[0m")

    newton_debug = {}
    try:
        newton_result = newton(test_func, test_func_deriv, 2.4, 0.0001, 0.0001, 1000, newton_debug)
    except ZeroDivisionError:
        newton_result = 'Newton method diverges.'

    print("Newton result: {}".format(newton_result))
    wait()
    print("Newton debug data:")
    pprint(newton_debug)
    wait()

    print_comment("Consistente com o resultado obtido previamente. (mais eficaz)")
    wait()

# ======  4 b) iii) b)
    print("\033[31m B) \033[0m")

    newton_debug = {}
    try:
        newton_result = newton(test_func, test_func_deriv, 1.4, 0.0001, 0.0001, 1000, newton_debug)
    except ZeroDivisionError:
        newton_result = 'Newton method diverges.'
    except ValueError as e:
        newton_result = 'Newton method is uncomputable: {}'.format(e)

    print("Newton result: {}".format(newton_result))
    wait()
    print("Newton debug data:")
    pprint(newton_debug)
    wait()

    print_comment("""
Verifica-se que o método de Newton não funciona para esta função,
uma vez que requer valores fora do domínio da função, após a 1a iteração;
a derivada é tal que a interpolação é avaliada a x<0, fora do domínio.
    """)
    wait()

# ======  Ex. 4 c)
    print_ex_label("4c)")

    print_comment("""
Observando o plot do gráfico previamente feito,
verifica-se que o zero no intervalo [0.75 : 1.75] encontra-se em boas
condições para ser aplicado o método de Newton.

Usando x = 0.75,
    """)

    wait()

    newton_debug = {}
    newton_result = newton(test_func, test_func_deriv, 0.75, 0.0001, 0.0001, 1000, newton_debug)

    print("Newton result: {}".format(newton_result))
    wait()
    print("Newton debug data:")
    pprint(newton_debug)
    wait()