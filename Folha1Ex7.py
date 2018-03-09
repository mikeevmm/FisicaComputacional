# ~*~ encoding:utf-8 ~*~

"""
Nos casos particulares que procuro optimizar, ie

n = 10000       m = 5000
n = 100000      m = 50000

tem-se que m = n/2.

Verificando que

m! = m*(m-1)*(m-2)*...*2*1

podemos reescrever o fatorial na forma

m! = (n)/2 * (n-2)/2 * (n-4)/2 * ... * 2 * 1

ou fatorizando 1/2^m

m! = (1/2)^(n/2) * n!! = (1/2)^(n/2) * n*(n-2)*(n-4)*...*2 =
    = (1/2)^(n/2) * 2 * 4 * 6 * ... * n

Tomando a expressão total ficamos com

0.5^(n-n/2) * (n * (n-1) * ... * (n - n/2 + 1)) / (n * (n-2) * (n-4) * ...)

ou simplificando

0.5^(n/2) * ((n-1) * (n-3) * ... * (n/2+1)) / ((n/2) * (n/2 - 2) * ... * 1)

ou à custa de m

0.5^(m) * ((2m-1) * (2m-3) * ... * (m+1)) / (m * (m-2) * ... * 1)

Podemos agora aplicar o logaritmo a toda a expressão, tal que ( L = log2 )

LP(m) = -m + L(2m-1) + L(2m-3) + ... + L(m+1) - [L(m) + L(m-2) + ... + L(2)]
"""

from math import log2

def P (m : int):
    return 2**(-m + sum(log2(x) for x in range(m+1, 2*m, 2)) - sum(log2(x) for x in range(2, m+1, 2)))

if __name__ == '__main__':
    import sys
    from time import clock
    
    in_val = int(sys.argv[1])
    start = clock()
    val = P(in_val)
    end = clock()
    print("binom({} {}) = {}".format(int(sys.argv[1])*2, int(sys.argv[1]), val) )
    print("⏲️ Took " + str(end - start) + " seconds. ⏰")