"""
Runs in about 30 seconds (lab computer).

We see the plot perfectly matches the theoretical prediction.
"""

from random import randint
from plot import plot
from time import clock

n = 10_000_000

start = clock()

throw_count = [0 for i in range(2, 13)]

for i in range(n):
    throw_count[sum(randint(1,6) for _ in range(2))-2] += 1

print("Took {} seconds.".format(clock() - start))

plot(tuple(i for i in range(2,13)), throw_count, 'w l')