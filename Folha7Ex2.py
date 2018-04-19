# -*- coding:utf-8 -*-

import numpy as np

def get_permutation (pivot_table):
    return np.matrix(
        tuple(
            tuple((0,)*pivot_table[i] + (1,) + (0,)*(len(pivot_table)-pivot_table[i]-1))
        for i in range(len(pivot_table))
        )
    )

def LU (matrix : np.matrix):
    """Returns the (L, U, pivot_table) decomposition of given matrix.

    Partial pivoting can be used.
    This expects an np.matrix and returns a tuple
    (L, U, pivot_table):"""
    # Dimensions
    dim_x, dim_y = matrix.shape
    if dim_x != dim_y:
        raise ValueError("Cannot LU non square matrix!")
    # i->i (identity) pivot_table
    pivot_table = np.arange(0, dim_y, 1)

    L = np.zeros((dim_x, dim_y), float)
    U = matrix # Not using copy for perf. and because arg should be ref anyway...
    L, U = L.astype(float), U.astype(float) # Avoid troublesome casts

    # Triangularization
    for j in range(dim_x-1):
        # Consider partial pivot
        pivot = max(range(j, dim_y), key=lambda i: np.abs(U[pivot_table[i],j]))
        prev = pivot_table[j]
        pivot_table[j] = pivot_table[pivot]
        pivot_table[pivot] = prev
        # Eliminate and store coefficients
        for i in range(j+1, dim_y):
            coef = U[pivot_table[i],j]/U[pivot_table[j],j]
            L[i, pivot_table[j]] = coef
            U[pivot_table[i],:] -= U[pivot_table[j],:]*coef
 
    # L starts as an identity matrix but has its columns
    #  shifted around; so we only set the "diagonal" to 1
    #  at the end.
    L[np.arange(dim_x), pivot_table] = 1.0

    # Done
    return (L, U, pivot_table)

if __name__ == '__main__':
    A = np.matrix('1 1 2; 3 5 9; 4 2 1')
    L,U,pivot_table = LU(A)
    P = get_permutation(pivot_table)

    print('P')
    print(P)
    print('L')
    print(L)
    print('U')
    print(U)
    print('A')
    print(A)
    print('L.U')
    print(L@U)
    print('P.L.U')
    print(P@L@U)