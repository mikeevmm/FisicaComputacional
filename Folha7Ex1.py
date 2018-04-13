# -*- coding:utf-8 -*-

import numpy as np

def solve(A : np.matrix, b : np.matrix):
    """Solve matrix equation system  Ax = b  for x.
    
    This assumes A and b are given in np.matrix form.
    This returns an np.matrix.
    """
    # Horizontal (i index) and vertical (j index) size
    a_x, a_y = A.shape
    # Pivoted to "true" matrix horizontal index
    #  initialized to i->i (identity)
    pivot_table = np.arange(0, a_x, 1)
    # Get extended matrix
    extended_matrix = np.concatenate((A, b), axis=1)
    # Triangularization:
    for j in range(0, a_x - 2):
        # Consider parcial pivot
        swap = max(range(j+1, a_y), key=lambda x: abs(extended_matrix[x,j])) # swap (j,j) with (swap,j)
        prev = pivot_table[j]
        pivot_table[j] = pivot_table[swap]
        pivot_table[swap] = prev
        # Zero elements below
        for i in range(j+1, a_y):
            extended_matrix[pivot_table[i],:] = np.add(
                extended_matrix[pivot_table[i],:],
                -extended_matrix[pivot_table[j],:]/extended_matrix[pivot_table[j],j]*extended_matrix[pivot_table[i],j],
                casting='unsafe' # np forces to disable safe casting due to int-float ops.
            )
            print(pivot_table)
            print(extended_matrix)
    # Retro elimination
    result = np.zeros((a_x, 1))
    for i in range(a_x-1, -1, -1):
        result[i] = (
            extended_matrix[pivot_table[i],-1] - sum(extended_matrix[pivot_table[i],j]*result[j] for j in range(i+1, a_x))
            )/extended_matrix[pivot_table[i],i]
    return result

if __name__ == '__main__':
    print('SANITY TEST ---')
    A = np.matrix('1 0 0 0; 0 1 0 0; 0 0 1 0; 0 0 0 1')
    b = np.matrix('1; 1; 1; 1')
    print(solve(A,b))
    exit()
    A = np.matrix('0 0 0 1; 0 1 0 0; 1 0 0 0; 0 0 1 0')
    b = np.matrix('1; 1; 1; 1')
    print(solve(A,b))
    print('YOUR STUFF ---')
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