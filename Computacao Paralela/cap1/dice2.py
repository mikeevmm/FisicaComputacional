from mpi4py import MPI
from random import randint

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

v = randint(1, 6)

if rank == 0:
    print ('Number of processes:', MPI.COMM_WORLD.Get_size())
    D = {}
    for i in range(1, 7):
        D[i] = 0
    print('On process', rank, 'value is', v)
    D[v] += 1
    for p in range(1, MPI.COMM_WORLD.Get_size()):
        v = comm.recv(source=p)
        print('On process', p, 'value is', v)
        D[v] += 1
    print ('Final result:', D)
else:
    comm.send(v, dest=0)


