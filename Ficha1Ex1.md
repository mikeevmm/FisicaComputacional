# Ex. 1

## a)

Na soma de dois números não inteiros é necessário o alinhamento ao maior expoente. Isto significa que para dois números de ordem de grandeza muito diferente

A = a.aaa E c
B = b.bbb E 0

c >> b

ao exprimir ambos os números com expoente 10^c, obtém-se

A = a.aaa E b
B = 0.000000 ... 0bbbb E c

Uma vez que a precisão dos números é limitada, e sendo a soma agora efetuada na mantissa, o valor de B poderá ser descartado na operação, resultando que

A + B = A

No caso particular dado, e tendo em conta que as operações são sequenciais,

     x + e
<=>  1 + 1E-20
<=>  1 + 0.000...1 ≈ 1

     x + e - x
<=>  (1 + 1E-20) - 1
<≈>  1 - 1 = 0

     e + x - x
<=>  (1E-20 + 1) - 1
<≈>  1 - 1 = 0

     x - x + e
<=>  (1 - 1) + 1E-20
<=>  0 + 1E-20 = 1E-20

## b)

Se e=0.01, a sua ordem de grandeza seria semelhante, e não se perderiam os bits de `e` na soma ou subtração. Nesse caso, será de esperar que todas as operações acima deem os valores corretos esperados.
