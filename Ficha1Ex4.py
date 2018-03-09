# ~*~ encoding:utf-8 ~*~

from functools import reduce

def factorial(n : int):
    if n == 0:
        return 1
    return reduce(lambda x,y: x*y, range(1, n+1))

def binom(n : int, m : int):
    return factorial(n)/(factorial(m) * factorial(n - m)) * 0.5**n

# Testing
if __name__ == '__main__':
    import sys
    print(binom(int(sys.argv[1]), int(sys.argv[2])))