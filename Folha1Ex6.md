A utilização da função fatorial três vezes não é, de facto, eficiente, verificando que

É imposto que n > m, então

    n! = n*(n-1)*...*(n-m)! =>

=>  binom(n,m) = n!/(m! * (n-m)! ) * (1/2)**n =
                = n*(n-1)*(n-2)*...*(n-m)!/(m! * (n-m)! ) * (1/2)**n =
                = n*...*(n-m+1)/m! * (1/2)**n

Esta optimização melhora em muito a capacidade de tratar números grandes, uma vez que o tamanho do numerador passa a crescer polinomialmente com `n`, e o denominador passa a crescer com m!, em vez de ~(m! * n!).