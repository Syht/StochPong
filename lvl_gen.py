# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 13:35:59 2017

@author: Syht
"""
import numpy as np
import os

np.set_printoptions(threshold=np.nan)
N_bricks = 81

x = 1
while x < 7:
    """ Creation of lvl 1 """
    if x == 1:
        p_ordered = np.ones(N_bricks)
    """ Creation of lvl 2 """
    if x == 2:
        p_ordered = np.hstack((1*np.ones(N_bricks//2), 5*np.ones(N_bricks//2), 0))
    """ Creation of lvl 3 """
    if x == 3:
        p_ordered = np.hstack((1*np.ones(N_bricks//4), 5*np.ones(N_bricks//4), 3*np.ones(N_bricks//2), 0))
    """ Creation of lvl 4 """
    if x == 4:
        p_ordered = np.hstack((2*np.ones(N_bricks//2), 4*np.ones(N_bricks//2), 0))
    """ Creation of lvl 5 """
    if x == 5:
        p_ordered = np.hstack((1*np.ones(N_bricks//4), 2*np.ones(N_bricks//4), 3*np.ones(N_bricks//4), 4*np.ones(N_bricks//4), 0))
    """ Creation of lvl 6 """
    if x == 6:
        p_ordered = np.hstack((1*np.ones(N_bricks//5), 2*np.ones(N_bricks//5), 3*np.ones(N_bricks//5), 4*np.ones(N_bricks//5), 5*np.ones(N_bricks//5), 0))

    x += 1

    np.random.seed(42)
    p_randomized = np.random.permutation(p_ordered).reshape((9,9))

    with open(os.path.join('lvl.npy'), 'a') as data:
        data.write('%s\n\n' %np.array2string(np.array(p_randomized).astype(int), separator=', '))