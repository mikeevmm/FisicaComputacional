from mpi4py import MPI
from random import randint

n = 100000000//2

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

D = {}
for i in range(1, 7):
    D[i] = 0
    
for i in range(n):
    v = randint(1, 6)
    D[v] += 1

if rank == 0:
    print ('Number of processes:', MPI.COMM_WORLD.Get_size())
    print('On process', rank, 'result is', D)
    for p in range(1, MPI.COMM_WORLD.Get_size()):
        Dp = comm.recv(source=p)
        print('On process', p, 'result is', Dp, sum(Dp[k] for k in Dp))
        for i in range(1, 7):
            D[i] += Dp[i]
    print ('Final result:         ', D, sum(D[k] for k in D))
else:
    comm.send(D, dest=0)


