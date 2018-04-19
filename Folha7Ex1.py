# -*- coding:utf-8 -*-

import numpy as np

def print_privoted (matrix, pivot_table):
    a_x, a_y = matrix.shape
    print('---')
    print( '\n'.join('\t'.join(str(matrix[pivot_table[u],w]) for w in range(a_y)) for u in range(a_x)) )
    print('---')

def solve(A : np.matrix, b : np.matrix):
    """Solve matrix equation system  Ax = b  for x.
    
    This assumes A and b are given in np.matrix form.
    This returns an np.matrix.
    """
    # Use floats
    A = A.astype(float)
    b = b.astype(float)
    # Horizontal (i index) and vertical (j index) size
    a_x, a_y = A.shape
    # Pivoted to "true" matrix horizontal index
    #  initialized to i->i (identity)
    pivot_table = np.arange(0, a_y, 1)
    # Get extended matrix
    extended_matrix = np.concatenate((A, b), axis=1)
    # Triangularization:
    for j in range(0, a_x-1):
        # Consider partial pivot
        pivot = max(range(j, a_y), key=lambda i: np.abs(extended_matrix[pivot_table[i],j]))
        prev = pivot_table[j]
        pivot_table[j] = pivot_table[pivot]
        pivot_table[pivot] = prev
        # Eliminate
        for i in range(j+1, a_y):
            np.add(
                extended_matrix[pivot_table[i],:],
                -extended_matrix[pivot_table[j],:]/extended_matrix[pivot_table[j],j]*extended_matrix[pivot_table[i],j],
                out=extended_matrix[pivot_table[i],:]
            )

    # Retro elimination
    # at this point, the *swapped* matrix is diagonal
    # Note that only lines were swapped, so the result
    #  vector does not need to reference pivot_table
    result = np.zeros((a_x, 1))
    for i in range(a_y-1, -1, -1):
        result[i] = (
            extended_matrix[pivot_table[i],-1] - sum(extended_matrix[pivot_table[i],j]*result[j] for j in range(i+1,a_x))
        )/extended_matrix[pivot_table[i],i]
    return result

if __name__ == '__main__':
    SQRT2 = np.sqrt(2)
    A = np.matrix((
        (-SQRT2, 2, 0),
        (1, -SQRT2, 1),
        (0, 2, -SQRT2)
    ))
    b = np.matrix((
        (1,),
        (1,),
        (1,)
    ))
    result = solve(A,b)
    print(result)