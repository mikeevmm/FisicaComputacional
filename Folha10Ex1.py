# -*- coding:utf-8 -*-

import urllib.request as urlreq
import numpy as np
import matplotlib.pyplot as plt
from functools import reduce

from Folha9Ex1 import min_sqrs
from Folha8Ex1 import ErrorValue

# URL of data file
URL = "http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/COURTEAU/catalogue/courteau99.dat"

# Labels of variables ( (x,y) ) to correlate
CORRELATE_VARS = ('vlg', 'L_B')

def get_r_sqrd (x_points : np.array, y_points : np.array):
    assert(len(x_points) == len(y_points))
    n = len(x_points)
    Sx = np.sum(x_points)
    Sy = np.sum(y_points)
    Sxy = sum(x_points[i]*y_points[i] for i in range(n))
    Sx2 = np.sum(x_points**2)
    Sy2 = np.sum(y_points**2)
    return (n*Sxy-Sx*Sy)**2/(n*Sx2-Sx**2)/(n*Sy2-Sy**2)

if __name__ == '__main__':

    assert(len(CORRELATE_VARS) == 2)

    x_points = []
    y_points = []
    
    with urlreq.urlopen(URL) as http_req:
        # Find index of vars to correlate
        labels = next(http_req).decode('UTF-8').split()
        x_index, y_index = (labels.index(var) for var in CORRELATE_VARS) 
        
        # Skip indexes
        next(http_req)

        # Read to end and grab x,y points
        for line in http_req:
            line = line.split()
            x_points.append(float(line[x_index]))
            y_points.append(float(line[y_index]))
    
    x_points = np.array(x_points)
    y_points = np.array(y_points)
    n = len(x_points)

    b,a = min_sqrs(x_points, y_points, 1)
    approx_x = np.arange(min(x_points), max(x_points))
    approx_y = a*approx_x + b

    r2 = get_r_sqrd(x_points, y_points)
    r = np.sqrt(r2) * np.sign(a)

    print('Determination coefficient:')
    print(r2)
    print('Relation coefficient:')
    print(r)

    # @ 95% confidence, t_c = 2.365
    tc = 2.365
    t = np.sqrt(r2*(n- 2)/(1 - r2)) # Actually abs of t

    print('T-Test absolute value:')
    print(t)

    print('With 95% certainty, there is{} correlation between the given variables.'.format('n\'t sufficient evidence of' if t < tc else ''))

    x_avg = np.average(x_points)
    delta = tc * np.sqrt(sum((a*x_points[i] + b - y_points[i])**2 for i in range(n))/sum(x_points[i]**2 - n*x_avg for i in range(n))/(n-2))

    a_with_err = ErrorValue(a, delta)
    print('With 95% certainty, the linear relation of the data has slope:')
    print(a_with_err)

    plt.plot(x_points, y_points, 'o')
    plt.plot(approx_x, approx_y, label='y = a+b*x,\na={:4E}\nb={:4E}'.format(a,b))
    plt.legend(loc='best')
    plt.show()