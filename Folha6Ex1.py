# -*- coding:UTF-8 -*-

from math import inf
import numpy as np

def gauss_elimination (extended_matrix):
    '''
    Triangularize an extended matrix.
    This assumes the matrix is represented as
        a list of np arrays, in the format
        of list of lines.
    This is not optimized.
    Returns triangularized matrix.
    '''
    v_length, h_length = len(extended_matrix), len(extended_matrix[0])
    if v_length != h_length - 1:
        raise ValueError('Cannot triangularize a non square coefficient matrix.')
    for j in range(0, v_length):
        # Eliminate (j-1,ith) element
        for i in range(j + 1, v_length):
            extended_matrix[i] = extended_matrix[i] - extended_matrix[j]/extended_matrix[j][j]*extended_matrix[i][j]
    return extended_matrix

def get_solution (triangularized_matrix):
    '''
    Returns the vector of solutions given
        a triangularized extended matrix.
    This assumes the matrix is represented as
        a list of np arrays, in the format
        of list of lines.
    If the matrix is not yet triangularized,
        call `gauss_elimination` first. 
    This is not optimized.
    '''
    v_length, h_length = len(triangularized_matrix), len(triangularized_matrix[0])
    solutions = make_matrix(1, v_length)
    for j in range(v_length - 1, -1, -1):
        solutions[j][0] = triangularized_matrix[j][h_length - 1] - sum(triangularized_matrix[j][i]*solutions[i] for i in range(j))
    return solutions

def make_matrix (n, m):
    '''
    Horizontal n
    Vertical m
    '''
    matrix = []
    for j in range(m):
        matrix.append(np.empty(n))
    return matrix

def as_matrix (obj):
    h_size = len(obj[0]) if hasattr(obj[0], '__len__') else 1
    v_size = len(obj) if hasattr(obj, '__len__') else 1
    matrix = make_matrix(h_size, v_size)
    if hasattr(obj, '__iter__'):
        for i in range(v_size):
            if hasattr(obj[i], '__iter__'):
                for j in range(v_size):
                    matrix[i][j] = obj[i][j]
            else:
                matrix[i][j] = obj[i]
    else:
        matrix[i][j] = obj
    return matrix


def matrix_mult (A, B):
    result = make_matrix(len(B[0]), len(A))
    print(result)
    for j in range(len(result)):
        for i in range(len(result[0])):
            result[j][i] = np.sum(A[j] * np.asarray(tuple(B[u][i] for u in range(len(B)))))

if __name__ == '__main__':

    extended_matrix = make_matrix(5,4)
    extended_matrix[0] = np.array((2, 2, 1, 4, 5))
    extended_matrix[1] = np.array((1, -3, 2, 3, 2))
    extended_matrix[2] = np.array((-1, 1, -1, -1, -1))
    extended_matrix[3] = np.array((1, -1, 1, 2, 2))

    triangularized = gauss_elimination(extended_matrix)
    solution = get_solution(triangularized)
    
    coef_matrix = make_matrix(4,4)
    coef_matrix[0] = np.array((2, 2, 1, 4))
    coef_matrix[1] = np.array((1, -3, 2, 3))
    coef_matrix[2] = np.array((-1, 1, -1, -1))
    coef_matrix[3] = np.array((1, -1, 1, 2))

    matrix_mult(coef_matrix, solution)
