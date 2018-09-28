#!/usr/bin/env python3

def plot(x_range, y_range, options = ''):
    assert(len(x_range)==len(y_range))
    from subprocess import call 
    with open('/tmp/plot.data', 'w') as tmp_file:
        tmp_file.write('\n'.join('{} {}'.format(x_range[i], y_range[i]) for i in range(len(x_range))))
    call('gnuplot -e \'plot "/tmp/plot.data" %s; pause -1\'' % options, shell=True) 

