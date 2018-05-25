#!/usr/bin/env python

# -*- coding:utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from random import random

# Initial count of nucleus (NucA, NucB, ...)
nucs = [100000, 0, 0]
# Decay values for each species (DecayA, DecayB, ...)
# (s⁻¹)
decay = (0.1, 0.3, 0)

# Time range (s)
t_values = np.arange(100)

nucs_values = np.zeros((len(nucs), len(t_values)))

assert(len(nucs) == len(decay))

nucs_values[:,0] = nucs
step_vals = np.zeros(len(nucs), int)
halflife = np.zeros(len(nucs))
halflife_population = np.round(nucs_values[:,0]/2)

for t in range(1, len(t_values)):
    step_vals[:] = nucs
    for i in range(len(nucs) - 1):
        for _ in range(nucs[i]):
            if random() < decay[i]:
                step_vals[i] -= 1
                step_vals[i+1] += 1
    nucs = step_vals[:]
    nucs_values[:,t] = nucs
    
    halflife[np.where((nucs_values[:,t-1] >= halflife_population) & (nucs_values[:,t] <= halflife_population))] = t

for i in range(len(nucs)):
    plt.plot(t_values, nucs_values[i,:], label='Nucleus {}'.format(i))
    plt.plot(t_values, np.ones(len(t_values)) * halflife_population[i], '--', label='Half of initial population ({})'.format(i))
plt.legend(loc='center right')
plt.show()

print("""
    According to the montecarlo simulation, the
    first nucleus's half life is {} s.
""".format(halflife[0]))
