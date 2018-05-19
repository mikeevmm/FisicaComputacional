# -*- coding:utf-8 -*-

from numbers import Number
from math import sqrt, log, log10, floor

class ErrorValue:

    def __init__(self, value, error):
        self._value = value
        self._error = abs(error)
        self.update_interval()
    
    def deltafunction(self, f):
        val = f(self.value)
        epsilon = val/100
        ddf = (f(val + epsilon) - f(val - epsilon))/2/epsilon
        return ErrorValue(val, abs(self.error * ddf))

    def update_interval(self):
        self.interval = (self.value - self.error, self.value + self.error)

    def get_value(self):
        return self._value
    def set_value(self, val):
        self._value = val
        self.update_interval()
    def get_error(self):
        return self._error
    def set_error(self, val):
        self._error = val
        self.update_interval()

    value = property(get_value, set_value)
    error = property(get_error, set_error)

    def __eq__(self, other):
        if isinstance(other, ErrorValue):
            if other.interval[0] > self.interval[1] or self.interval[0] > other.interval[1]:
                return False
            # else
            return True
        # else
        if isinstance(other, Number):
            return ErrorValue(other, 0) == self
        raise ValueError('Cannot compare ErrorValue with non numeric.')

    def __radd__(self, other):
        return self + other
    
    def __add__(self, other):
        if isinstance(other, ErrorValue):
            return ErrorValue(self.value + other.value, sqrt(self.error**2 + other.error**2))
        # else
        if isinstance(other, Number):
            return ErrorValue(self.value + other, self.error)
        raise ValueError('Cannot add ErrorValue to non numeric.')

    def __sub__(self, other):
        # self - other
        if isinstance(other, ErrorValue):
            return ErrorValue(self.value - other.value, sqrt(self.error**2 + other.error**2))
        # else
        if isinstance(other, Number):
            return ErrorValue(self.value - other, self.error)
        raise ValueError('Cannot subtract non numeric from ErrorValue.')
    
    def __rsub__(self, other):
        if isinstance(other, ErrorValue):
            return ErrorValue(other.value - self.value, sqrt(self.error**2 + other.error**2))
        # else
        if isinstance(other, Number):
            return ErrorValue(other - self.value, self.error)
        raise ValueError('Cannot subtract non numeric from ErrorValue.')
    
    def __rmul__(self, other):
        return self*other

    def __mul__(self, other):
        if isinstance(other, ErrorValue):
            return ErrorValue(self.value*other.value, sqrt((other.value*self.error)**2 + (other.error*self.value)**2))
        # else
        if isinstance(other, Number):
            return ErrorValue(self.value * other, abs(other*self.error))
        raise ValueError('Cannot multiply ErrorValue by non numeric.')

    def __truediv__(self, other):
        if isinstance(other, ErrorValue):
            return ErrorValue(self.value/other.value, sqrt((self.error/other.value)**2 + (self.value/other.value**2*other.error)**2))
        # else
        if isinstance(other, Number):
            return ErrorValue(self.value/other, self.error/abs(other))
        raise ValueError('Cannot divide ErrorValue by non numeric.')
    
    def __rtruediv__(self, other):
        # other / self
        if isinstance(other, ErrorValue):
            return ErrorValue(other.value/self.value, sqrt((other.error/self.value)**2 + (other.value/self.value**2*self.error)**2))
        # else
        if isinstance(other, Number):
            return ErrorValue(other/self.value, abs(other/self.value**2*self.error))
        raise ValueError('Cannot divide ErrorValue by non numeric.')
    
    def __pow__(self, other):
        if isinstance(other, ErrorValue):
            pow_result = self.value**other.value
            return ErrorValue(pow_result, sqrt((other.value*self.value**(other.value-1)*self.error)**2+(pow_result*log(self.value)*other.error)**2))
        # else
        if isinstance(other, Number):
            return ErrorValue(self.value**other, abs(other*self.value**(other-1)*self.error))
        raise ValueError('Cannot raise ErrorValue to non numeric.')

    def __rpow__(self, other):
        if isinstance(other, ErrorValue):
            pow_result = other.value**self.value
            return ErrorValue(pow_result, sqrt((self.value*other.value**(self.value-1)*other.error)**2+(pow_result*log(other.value)*self.error)**2))
        # else
        if isinstance(other, Number):
            return ErrorValue(other**self.value, abs(other**self.value*log(other)*self.error))
        raise ValueError('Cannot raise non numeric to ErrorValue.')
    
    def __repr__(self):
        if self.error > self.value:
            # Odd, but:
            err_expnt = floor(log10(self.error))
            str_error = str(self.error/10**err_expnt)[0]
            return '0({}){}'.format(str_error, 'E' + str(err_expnt) if err_expnt != 0 else '')
        value_expnt = floor(log10(self.value))
        base_err = '{:f}'.format(self.error*10**(-value_expnt)) # Force non sci
        base_value = '{:f}'.format(self.value*10**(-value_expnt)) # ""
        decimals = 0
        # usual error string
        while len(set(base_err[:decimals+1]) - set('0.')) == 0:
            decimals += 1
        str_error = base_err[decimals]
        # 1 case
        if base_err[decimals] == '1' and len(base_err) > decimals and base_err[decimals + 1] != '.':
            str_error += base_err[decimals + 1]
            decimals += 1
        str_value = base_value[:decimals + 1]
        # round up if needed
        if len(base_err) > decimals + 1:
            if base_err[decimals + 1] == '.':
                if len(base_err) > decimals + 2:
                    if int(base_err[decimals + 2]) > 5:
                        str_error = str_error[:-1] + str(int(str_error[-1]) + 1)
            else:
                if int(base_err[decimals + 1]) > 5:
                    str_error = str_error[:-1] + str(int(str_error[-1]) + 1)
        # We don't need to check for rounding @ last digit of
        #  of value, because error is at least 1 @ that position.
        # Add extra zeros if needed
        if decimals + 1 > len(str_value):
            str_value += '0'*(len(str_value) + 1 - decimals)
        return '{}({}){}'.format(str_value, str_error, 'E' + str(value_expnt) if value_expnt != 0 else '')

if __name__ == '__main__':
    # Rounding test
    print(ErrorValue(2,1.9))
    
    # Ops test
    a = ErrorValue(1, 0.012)
    b = ErrorValue(40, 20)

    print('a')
    print(a)
    print('b')
    print(b)

    print('a == b')
    print(a == b)

    print('a == 1.1')
    print(a == 1.1)

    print('a == 100')
    print(a == 100)

    print('b == 1')
    print(b == 1)

    print('a*b')
    print(a*b)

    print('a*2')
    print(a*2)

    print('3*b')
    print(3*b)

    print('a/b')
    print(a/b)

    print('b/2')
    print(b/2)

    print('2/a')
    print(2/a)

    print('b**2')
    print(b**2)

    print('a**b')
    print(a**b)

    print('4**a')
    print(4**a)

    print('x**2 @ {}'.format(a))
    f = lambda x: x**2
    print(a.deltafunction(f))