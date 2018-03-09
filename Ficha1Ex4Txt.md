# a)

python Ficha1Ex4.py 100 6
9.403635353348797e-22

python Ficha1Ex4.py 15 2
0.003204345703125

python Ficha1Ex4.py 58 32
0.07684950331601552

python Ficha1Ex4.py 2 1
0.5

## b)

python Ficha1Ex4.py 100 0
7.888609052210118e-31

python Ficha1Ex4.py 100 50
0.07958923738717877

Conclui-se que é mais provável obter 50 caras.

## c)

python Ficha1Ex4.py 10000 5000
Traceback (most recent call last):
  File "Ficha1Ex4.py", line 16, in <module>
    print(binom(int(sys.argv[1]), int(sys.argv[2])))
  File "Ficha1Ex4.py", line 11, in binom
    return factorial(n)/(factorial(m) * factorial(n - m)) * 0.5**n
OverflowError: integer division result too large for a float

Os valores obtidos são demasiado grandes para serem convertidos para float.