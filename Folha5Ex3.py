# -*- coding: utf-8 -*-

def get_spline_interpolation (data):
    # Find coefficients
    n = len(data) - 1
    c1 = []
    c2 = []
    c3 = []
    c4 = []
    h = []
    z = []
    d = [None] # 1-indexed
    b = [None] # 1-indexed
    m = [0 for i in range(n + 1)]
    for i in range(0, n):
        h.append(data[i+1][0] - data[i][0])
        z.append((data[i+1][1] - data[i][1])/h[i])
    d.append(2*(h[0] + h[1]))
    b.append(6*(z[1] - z[0]))
    for i in range(2, n):
        M = h[i-1]/d[i-1]
        d.append(2*(h[i-1]+h[i]) - M*h[i-1])
        b.append(6*(z[i] - z[i-1]) - M*b[i-1])
    m[n-1] = b[n-1]/d[n-1]
    for i in range(n-2, 0, -1):
        m[i] = (b[i] - h[i] * m[i+1])/d[i]
    for i in range(0, n):
        c1.append(data[i][1])
        c2.append(z[i]-h[i]/6*(m[i+1] + 2*m[i]))
        c3.append(m[i]/2)
        c4.append((m[i+1]-m[i])/(6*h[i]))
    # Return function
    segments = tuple((data[x][0], data[x+1][0]) for x in range(n - 1))
    def interpolated(x):
        for i in range(len(segments)):
            k = i            
            if x >= segments[i][0] and x < segments[i][1]:
                break
        return c1[k] + (x - data[k][0]) * (c2[k] + (x - data[k][0]) * (c3[k] + (x - data[k][0])*c4[k]))
    return interpolated

if __name__ == '__main__':

    import matplotlib.pyplot as plt
    import numpy as np
    from math import pi

    data = (
        (1920,    106.46),
        (1930,    123.08),
        (1940,    132.12),
        (1950,    152.27),
        (1960,    180.67),
        (1970,    205.05),
        (1980,    227.23),
        (1990,    249.46),
        (2000,    281.42)
    )

    interpolation = get_spline_interpolation(data[:-1])

    xrange = np.arange(1900, 2010, 0.01)
    
    interpolation_y = tuple(
        interpolation(x) for x in xrange
    )
    plt.plot(xrange, interpolation_y, label='Spline interpolation.')
    plt.plot(tuple(x[0] for x in data), tuple(x[1] for x in data), 'o', label='Data (1920 - 1990)')
    plt.legend(loc='best')
    plt.show()

    print('''\
Clearly, the spline interpolation is much more useful to extrapolate
the available data.

Predicted population for 2000: {}
Actual population for 2000: {}
Absolute error: {}
Error (%) : {}
    '''.format(
        data[-1][1],
        interpolation(2000),
        abs(data[-1][1] - interpolation(2000)),
        abs(data[-1][1] - interpolation(2000))/data[-1][1])
    )