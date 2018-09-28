#!/usr/bin/env python3

"""
Runs in about 8 seconds (lab computer).
That's about three times faster than in single core.
"""

from random import randint
import numpy as np
from time import clock
from mpi4py import MPI

# -- params

n = 10_000_000

# -- body

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    start = clock()

core_count = comm.Get_size()
n_core = n//core_count

if rank == 0:
    n_core += n - n_core*core_count

print("Rank {} is responsible for {} throws".format(rank, n_core))

throw_count = np.zeros(12)

for i in range(n_core):
    throw_count[sum(randint(1,6) for _ in range(2))-2] += 1

print("I'm ({}) done.".format(rank))

if rank == 0:
    for core in range(1, core_count):
        throw_count += comm.recv(source=core)
    print("Result:")
    print(throw_count)
    print("Took {} seconds".format(clock() - start))
else:
    comm.send(throw_count, dest=0)