from random import randint

n = 10
D = {}
for i in range(1, 7):
    D[i] = 0
    
for i in range(n):
    v = randint(1, 6)
    print (v)
    D[v] += 1

print (D)
