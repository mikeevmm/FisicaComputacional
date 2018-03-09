# ~*~ encoding:utf-8 ~*~

"""
O programa abaixo não termina devido à representação binária de 0.1.

De facto, em base 2, 0.1 é uma dízima infinita; convertendo o número para base 2:

(0.1)b10 = (0.0001 1001 1001 1001 1001 1001 1001 ...)b2

Ao somar `d` repetidamente a x, e sendo a precisão de floats finita,
acumula-se erro suficiente para que (x == 1.0) (com 1.0 infinitamente preciso)
não seja verdade.

Isto é visível no output, onde para valores como 0.3, 0.8, 0.9, 1.0 o erro
já é visível.

``` Output
0.0
0.1
0.2
0.30000000000000004
0.4
0.5
0.6
0.7
0.7999999999999999
0.8999999999999999
0.9999999999999999
```

É possível obter o valor esperado modificando o programa para fixar 2
casas decimais, como feito abaixo.

(Poder-se-ia também testar para x < 1.0)
"""

d = 0.1
x = 0.0
while x != 1.0:
    print(x)
    x += d
    x = round(x, 3)