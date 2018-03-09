# ~*~ encoding:utf-8 ~*~

from functools import reduce

def factorial(n : int):
    if n == 0:
        return 1
    return reduce(lambda x,y: x*y, range(2, n+1))

def binom(n : int, m : int):
    return factorial(n)/(factorial(m) * factorial(n - m)) * 0.5**n

def binomsum(n : int):
    return sum(binom(n, m) for m in range(0, n+1))

# Testing
if __name__ == '__main__':
    print(*('n:{}\tbinomsum(n):{}'.format(n, binomsum(n)) for n in range(0, 1000, 30)), sep='\n')
    print('Dá aproximadamente correto, mas observam-se erros de arredondamento.')