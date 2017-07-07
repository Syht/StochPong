# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 10:24:13 2017

@author: Thys
"""

import os, matplotlib.pyplot as plt, numpy as np, pandas as pd, math

subjects = ['remi', 'valerie', 'jade', 'juliette', 'elisa', 'maxime']
t, x, y, time, fig = {}, {}, {}, [], []
dfs = {}

for subj in subjects:
    i = 1
    for file in os.listdir(os.path.join('datadir', 'pilot')):
        if file.endswith(".csv"):
            if subj in file:
                dfs['df%s%s' %(subj, i)] = pd.read_csv(os.path.join('datadir', 'pilot', file), '\t')
                i += 1

# The dataframes are in the variables named : df<subject_name><level_number> and stored in a dict
j = 0
for key, df in dfs.items():
    fig.append(fig)
    fig[j], ax = plt.subplots(figsize=(15,8))
    for obj, color in zip(['gaze', 'ball', 'paddle'], ['g', 'b', 'r']):
        if obj == 'gaze':
            t[obj], x[obj], y[obj] = df.loc[:,'Tgaze'], df.loc[:,'Xgaze'], df.loc[:,'Ygaze']
        if obj == 'ball':
            t[obj], x[obj], y[obj] = df.loc[:,'Tball'], df.loc[:,'Xball'], df.loc[:,'Yball']
        if obj == 'paddle':
            t[obj], x[obj], y[obj] = df.loc[:,'Tpaddle'], df.loc[:,'Xpaddle'], df.loc[:,'Ypaddle']
    j += 1
    time.append(t['gaze'][len(t['gaze'])-1] - t['gaze'][0]) # retrieve the lengths of the levels
    plt.plot(t['gaze']-t['gaze'][0], x['gaze'], 'g') # plot of time(Xgaze)
    plt.plot(t['paddle']-t['paddle'][0], x['ball'], 'b') # plot of time(Xball)
    plt.plot(t['paddle']-t['paddle'][0], x['paddle'], 'r') # plot of time(Xpaddle)
print(time)