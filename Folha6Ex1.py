# -*- coding:UTF-8 -*-

from math import inf
import numpy as np
from functools import reduce

def gauss_elimination (extended_matrix):
    """Triangularize an extended matrix.

    This assumes the matrix is represented as
        a list of np arrays, in the format
        of list of lines.
    This is not especially optimized.
    Returns triangularized matrix.
    """
    v_length, h_length = len(extended_matrix), len(extended_matrix[0])
    if abs(v_length - h_length) != 1:
        raise ValueError('Cannot triangularize a non square coefficient matrix.')
    for j in range(0, v_length - 1):
        for i in range(j + 1, v_length):
            extended_matrix[i] = extended_matrix[i] - extended_matrix[j]/extended_matrix[j][j]*extended_matrix[i][j]
    return extended_matrix

def make_extended_matrix (A, b):
    """Given a coefficient matrix A and result vector b, returns an extended matrix.

    This assumes the matrix is represented as
        a list of np arrays, in the format
        of list of lines.
    This is not especially optimized.
    """
    extended_matrix = make_matrix(len(A[0]) + 1, len(A))
    for j in range(len(extended_matrix)):
        for i in range(len(extended_matrix[j]) - 1):
            extended_matrix[j][i] = A[j][i]
        extended_matrix[j][-1] = b[j]
    return extended_matrix

def get_solution (triangularized_matrix):
    """Returns the vector of solutions given a triangularized extended matrix.

    This assumes the matrix is represented as
        a list of np arrays, in the format
        of list of lines.
    If the matrix is not yet triangularized,
        call `gauss_elimination` first. 
    This is not especially optimized.
    """
    v_length = len(triangularized_matrix)
    solutions = make_matrix(1,v_length)
    for j in range(v_length - 1, -1, -1):
        others = sum(triangularized_matrix[j][u] * solutions[u][0] for u in range(j + 1, v_length))
        solutions[j][0] = (triangularized_matrix[j][-1] - others)/triangularized_matrix[j][j]
    return solutions

def get_inverse (matrix):
    """Determines inverse matrix of given matrix.

    This assumes the matrix is represented as
        a list of np arrays, in the format
        of list of lines.
    This is not especially optimized.
    """
    # Get basis of matrix
    dim = len(matrix[0])
    basis = []
    for i in range(dim):
        basis.append(as_vector(
            (0,)*i + (1,) + (0,)*(dim - i - 1)
        ))
    # Solve for each vector
    sol = [
        get_solution(gauss_elimination(make_extended_matrix(matrix, versor)))
        for versor in basis
    ]
    # "Make" inverse
    result = make_matrix(len(basis), dim)
    for j in range(dim):
        for i in range(len(basis)):
            result[j][i] = sol[i][j]
    return result

def make_matrix (n, m):
    """Make a horizontal n by vertical m zero matrix."""
    matrix = []
    for _ in range(m):
        matrix.append(np.zeros(n))
    return matrix

def as_matrix (obj):
    h_size = len(obj[0]) if hasattr(obj[0], '__len__') else 1
    v_size = len(obj) if hasattr(obj, '__len__') else 1
    matrix = make_matrix(h_size, v_size)
    if v_size > 1:
        for i in range(v_size):
            if h_size > 1:
                for j in range(h_size):
                    matrix[i][j] = obj[i][j]
            else:
                matrix[i] = obj[i]
    else:
        matrix[0][0] = obj
    return matrix

def as_vector (vector):
    v_size = len(vector) if hasattr(vector, '__len__') else 1
    matrix = make_matrix(1, v_size)
    if v_size > 1:
        for i in range(v_size):
            matrix[i][0] = vector[i]
    else:
        matrix[0][0] = vector
    return matrix

def pprint_matrix(matrix):
    return 'MATRIX:\n\t' + '\n\t'.join('\t'.join(str(matrix[i][j]) for j in range(len(matrix[i]))) for i in range(len(matrix)))

def matrix_mult (A, B):
    """ Returns the matricial product of A,B """
    result = make_matrix(len(B[0]), len(A))
    for j in range(len(result)):
        for i in range(len(result[0])):
            result[j][i] = np.sum(A[j] * np.asarray(tuple(B[u][i] for u in range(len(B)))))
    return result

def get_identity(n):
    """Returns an nxn identity matrix."""
    matrix = make_matrix(n,n)
    for i in range(n):
        matrix[i][i] = 1
    return matrix

def compare_matrices(A,B):
    A_v_length, A_h_length = len(A), len(A[0])
    B_v_length, B_h_length = len(B), len(B[0])
    if A_v_length != B_v_length or A_h_length != B_h_length:
        return False
    return all(all(A[j] == B[j]) for j in range(len(A)))

if __name__ == '__main__':

    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Solves a linear eq. system.')
    parser.add_argument('file', nargs='?', help='File with matrix data (stdin by default)',
        type=argparse.FileType('r'), default=sys.stdin)
    args = parser.parse_args()

    with args.file as infile:
        b = infile.readline().split()
        A = tuple(x.split() for x in infile.read().split('\n'))

    coef_matrix = as_matrix(A)
    result_vec = as_vector(b)
    extended_matrix = make_extended_matrix(coef_matrix, result_vec)
    
    print('EXTENDED MATRIX')
    print(pprint_matrix(extended_matrix))

    triangularized = gauss_elimination(extended_matrix)
    print('TRIANGULARIZED MATRIX')
    print(pprint_matrix(triangularized))

    solution = get_solution(triangularized)
    print('SOLUTION')
    print(pprint_matrix(solution))

    result = matrix_mult(coef_matrix, solution)
    print('COEFFICIENT MATRIX X SOLUTION VECTOR')
    print(pprint_matrix(result))

    inverse = get_inverse(coef_matrix)
    print('COEFFICIENT MATRIX INVERSE')
    print(pprint_matrix(inverse))

    inverted_prod = matrix_mult(coef_matrix, inverse)
    print('INVERSE TEST')
    print(pprint_matrix(inverted_prod))

    print('IS EQUAL TO IDENTITY')
    print(compare_matrices(inverted_prod, get_identity(len(coef_matrix))))

    print('EX 3.:')
    
    SQRTT = np.sqrt(2)
    coef_matrix = as_matrix((
        (-SQRTT, 2, 0),
        (1, -SQRTT, 1),
        (0, 2, -SQRTT)
    ))
    extended_matrix = as_matrix((
        (-SQRTT, 2, 0, 1),
        (1, -SQRTT, 1, 1),
        (0, 2, -SQRTT, 1)
    ))

    triangularized = gauss_elimination(extended_matrix)
    print('TRIANGULARIZED MATRIX')
    print(pprint_matrix(triangularized))

    solution = get_solution(triangularized)
    print('SOLUTION')
    print(pprint_matrix(solution))

    result = matrix_mult(coef_matrix, solution)
    print('COEFFICIENT MATRIX X SOLUTION VECTOR')
    print(pprint_matrix(result))