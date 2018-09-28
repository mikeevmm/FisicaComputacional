from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    print ('Number of processes:', MPI.COMM_WORLD.Get_size())
    for p in range(1, MPI.COMM_WORLD.Get_size()):
        data = comm.recv(source=p)
        print('On process', p, 'data is', data)
else:
    data = {'rank': rank, 'value': 10*rank}
    comm.send(data, dest=0)
