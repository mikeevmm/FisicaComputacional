# -*- coding:utf-8 -*-

import numpy as np

def solve(A : np.matrix, b : np.matrix) -> np.matrix:
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

def min_sqrs(x : np.array, y : np.array, deg: int) -> np.array:
    """Returns a min square approximation to the deg-function yielding (x,y).

    Given points in the form of `x` array and `y` array,
    returns a `deg+1` length array of parameters `a_0 ... a_deg`
    such that
        `f(x) = a_0 + a_1 * x + ... + a_deg * x^(deg)` 
    """
    if len(x) != len(y):
        raise ValueError('Mismatched x, y array size.')

    A = np.zeros((deg + 1, deg + 1))
    b = np.zeros((deg + 1, 1))
    
    # Init A
    A_y, A_x = A.shape

    # Take advantage of the symmetry
    A[0,0] = len(x)
    for i in range(A_y):
        for j in range(i+1, A_x):
            coef = sum(x[u]**(i+j) for u in range(len(x)))
            A[i,j] = coef
            A[j,i] = coef
        A[i,i] = sum(x[u]**(2*i) for u in range(len(x))) # avoid double assignment
    
    # Init b
    b_y, b_x = b.shape
    b[0, 0] = sum(y[u] for u in range(len(y)))
    for i in range(1, b_y):
        b[i, 0] = sum(y[u]*x[u]**i for u in range(len(x)))

    # Solve system
    result = solve(A, b) # Column vector
    return result.T[0] # Standard array (bit hacky)

# Testing
if __name__ == '__main__':
    import matplotlib.pyplot as plt

    # Given data
    x = np.array((1,2,4,8,6,5,8,9,7))
    y = np.array((2,3,4,7,6,5,8,8,6))

    # Perform several deg. adjustments & plot
    for deg in range(1, 4):
        coefs = min_sqrs(x, y, deg)
        f = lambda x: sum(coefs[u]*x**u for u in range(len(coefs)))

        x_plt = np.linspace(-3, 12, 100)
        y_plt = f(x_plt)

        plt.plot(x_plt, y_plt, label='Pol. Deg. {}'.format(deg))
    plt.plot(x, y, 'o')
    plt.legend(loc='best')
    plt.xlim(-2, 11)
    plt.ylim(-2, 11)
    plt.show()

    # Using given data
    

