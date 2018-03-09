# ~*~ encoding:utf-8 ~*~

"""
a)

Tal como no exercício 1, para `n` suficientemente grande,
2.0E(-n) é muito menor do que 1.0 em ordem de grandeza, pelo que na
soma se perde o valor na mantissa do primeiro. Nesta situação,

1.0 + 2.0**(-n) - 1.0 ≃ 1.0 - 1.0 = 0.0

Neste caso o *loop* é quebrado, e o programa termina.

O último valor de `n` antes do programa terminar corresponde ao valor a seguir ao menor dígito
significativo, ou seja, o número de bits disponíveis na mantissa + 1.

Isto é perfeitamente compatível com a especificação IEEE 64-bit, onde a mantissa tem
disponíveis 64-13=52 bits.


b)

O valor de `n` representa agora o valor a partir do qual (inclusive) a mantissa é arredondada
a 0, depois do expoente ter sido "esgotado".

De acordo com a especificação IEEE 64-bit, o expoente tem 11 bits disponíveis (com 1 para sinal) e
a mantissa tem 52 bits disponíveis.
Assim, será de esperar que o último valor de `n` obtido seja 2^(11-1) + 52 - 1 = 1075,
o que se verifica exatamente.
"""

import math

n = 0
a = 1
while a > 0:
    n = n+1
    a = (1.0 + 2.0**(-n)) - 1.0
print( -int(math.log10(2.0**(-n+1)) ), 'algarismos significativos (decimais)')