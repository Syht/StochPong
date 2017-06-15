# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 13:35:59 2017

@author: Syht
"""
import numpy as np
import os

np.set_printoptions(threshold=np.nan)
N_bricks = 8*9
p_ordered = np.hstack((1*np.ones(N_bricks//2), 5*np.ones(N_bricks//2)))
np.random.seed(42)
p_randomized = np.random.permutation(p_ordered).reshape((9,8))

with open(os.path.join('lvl.npy'), 'w') as data:
    data.write('%s' %np.array2string(np.array(p_randomized).astype(int), separator=', '))