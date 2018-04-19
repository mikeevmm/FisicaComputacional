# -*- coding:utf-8 -*-

import numpy as np
from numbers import Number
from copy import copy

class SquareMatrix():
    def __init__(self, n : int = 0, c : dict = {}):
        self.c = c
        self.n = n
        self.__radd__=self.__add__ # Comutative addition
    def asnumpy(self):
        matrix = np.zeros((self.n, self.n), float)
        for i in range(self.n):
            for j in range(self.n):
                matrix[i,j] = self.c.get(i, {}).get(j, 0)
        return matrix
    def astuple(self):
        return tuple(
            tuple(
                self.c.get(i, {}).get(j,0) for j in range(self.n)
            ) for i in range(self.n)
        )
    def getdata(self, filename):
        with open(filename) as file:
            i = 0
            for line in file.read().split('\n'):
                j = 0
                for column in line.split():
                    self.c.setdefault(i, {})[j] = float(column)
                    j += 1
                i += 1
    def getinverse(self):
        matrix = self.asnumpy()
        extended = np.concatenate((matrix, np.identity(self.n, float)), axis=1)
        pivot_table = np.arange(self.n)
        for j in range(self.n - 1):
            pivot = max(range(j, self.n), key=lambda x: np.abs(extended[pivot_table[x],j]))
            prev = pivot_table[j]
            pivot_table[j] = pivot_table[pivot]
            pivot_table[pivot] = prev
            for i in range(j+1, self.n):
                np.add(
                    extended[pivot_table[i],:],
                    -extended[pivot_table[j],:]/extended[pivot_table[j],j]*extended[pivot_table[i],j],
                    out=extended[pivot_table[i],:]
                )
        result = np.zeros((self.n, self.n))
        for j in range(self.n):
            for i in range(self.n-1, -1, -1):
                result[i,j] = (
                    extended[pivot_table[i],self.n+j] - sum(extended[pivot_table[i],u]*result[u,j] for u in range(i+1,self.n))
                )/extended[pivot_table[i],i]
        return SquareMatrix(self.n, {i:{j:result[i,j] for j in range(self.n)} for i in range(self.n)})
    def computeLU(self):
        matrix = self.asnumpy()
        # i->i (identity) pivot_table
        pivot_table = np.arange(0, self.n, 1)

        L = np.zeros((self.n, self.n), float)
        U = matrix # Not using copy for perf. and because arg should be ref anyway...
        L, U = L.astype(float), U.astype(float) # Avoid troublesome casts

        # Triangularization
        for j in range(self.n-1):
            # Consider partial pivot
            pivot = max(range(j, self.n), key=lambda u: abs(U[pivot_table[u],j]))
            prev = pivot_table[j]
            pivot_table[j] = pivot_table[pivot]
            pivot_table[pivot] = prev
            # Eliminate and store coefficients
            for i in range(j+1, self.n):
                coef = U[pivot_table[i],j]/U[pivot_table[j],j]
                L[i, pivot_table[j]] = coef
                U[pivot_table[i],:] -= U[pivot_table[j],:]*coef
    
        # L starts as an identity matrix but has its columns
        #  shifted around; so we only set the "diagonal" to 1
        #  at the end.
        L[np.arange(self.n), pivot_table] = 1.0

        # To dicts
        self.L = {i:{j:L[i,j] for j in range(self.n)} for i in range(self.n)}
        self.U = {i:{j:U[i,j] for j in range(self.n)} for i in range(self.n)}

    def __add__(self, other):
        if type(other) is not SquareMatrix:
            return SquareMatrix(0)
            #raise ValueError("Cannot add SquareMatrix to other type.")
        if self.n != other.n:
            return SquareMatrix(0)
            #raise ValueError("Cannot add matrices of different size.")
        result = SquareMatrix(self.n, {})
        for i in set(self.c)|set(other.c):
            result.c[i] = {}
            for j in set(self.c.get(i,0))|set(self.c.get(i,0)):
                result.c[i][j] = self.c.get(i,{}).get(j,0) + other.c.get(i,{}).get(j,0) 
        return result
    def __sub__(self, other):
        if type(other) is not SquareMatrix:
            return SquareMatrix(0)
            #raise ValueError("Cannot subtract SquareMatrix from/to other type.")
        if self.n != other.n:
            return SquareMatrix(0)
            #raise ValueError("Cannot subtract matrices of different size.")
        result = SquareMatrix(self.n, {})
        # Assume non declared elements are 0
        for i in set(self.c)|set(other.c):
            result.c[i] = {}
            for j in set(self.c.get(i,0))|set(self.c.get(i,0)):
                result.c[i][j] = self.c.get(i,{}).get(j,0) - other.c.get(i,{}).get(j,0) 
        return result
    def __rmul__(self,other):
        if isinstance(other, Number):
            result = copy(self)
            for i in result.c:
                for j in result.c[i]:
                    result.c[i][j] *= other
            return result
        elif type(other) is not SquareMatrix:
            return SquareMatrix(0)
        return self*other
    def __mul__(self,other):
        if isinstance(other, Number):
            result = copy(self)
            for i in result.c:
                for j in result.c[i]:
                    result.c[i][j] *= other
            return result
        elif type(other) is not SquareMatrix:
            return SquareMatrix(0)
            #raise ValueError("Can onl multiply SquareMatrix by SquareMatrix or number.")
        if self.n != other.n:
            return SquareMatrix(0)
            #raise ValueError("Cannot multiply square matrices of different size.")
        result = SquareMatrix(self.n, {})
        for i in set(self.c)|set(other.c):
            result.c[i] = {}
            for j in set(self.c.get(i,0))|set(self.c.get(i,0)):
                result.c[i][j] = sum(self.c.get(i,{}).get(u,0)*other.c.get(u,{}).get(j,0) for u in range(self.n))
        return result
    def __str__(self):
        astuple = self.astuple()
        return '('+'\n '.join(str(astuple[i]) for i in range(self.n))+')'

if __name__ == '__main__':
    t = SquareMatrix(3, {})
    t.getdata('Folha7Ex3Test.txt')
    
    print('T:')
    print(t)

    print('Inverse')
    print(t.getinverse())

    print('I@t')
    print((t.getinverse()*t).astuple())
    
    print('LU')
    t.computeLU()
    L = SquareMatrix(3, t.L)
    U = SquareMatrix(3, t.U)
    print('L@U')
    print(L*U)