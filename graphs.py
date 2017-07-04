import os, matplotlib.pyplot as plt, numpy as np, pandas as pd

time, x, y = {}, {}, {}

datadir, tagg, subject = 'datadir', '2017-06-28_144217', 'juliette'
tags = ['2017-06-28_133727', '2017-06-28_134443', '2017-06-28_135020', '2017-06-28_135706', '2017-06-28_140322', '2017-06-28_141025']
fig = ['fig1', 'fig2', 'fig3', 'fig4', 'fig5', 'fig6']


i = 0
for tag in tags:
    fig[i], ax = plt.subplots(figsize=(15,8))
    df = pd.read_csv(os.path.join(datadir, tag + '_dataframe_' + subject + '.csv'), '\t')

    for obj, color in zip(['gaze', 'ball', 'paddle'], ['g', 'b', 'r']):
        if obj == 'gaze':
            time[obj], x[obj], y[obj] = df.loc[:,'Tgaze'], df.loc[:,'Xgaze'], df.loc[:,'Ygaze']
        if obj == 'ball':
            time[obj], x[obj], y[obj] = df.loc[:,'Tball'], df.loc[:,'Xball'], df.loc[:,'Yball']
        if obj == 'paddle':
            time[obj], x[obj], y[obj] = df.loc[:,'Tpaddle'], df.loc[:,'Xpaddle'], df.loc[:,'Ypaddle']
        ax.set_xlim([-100,1300])
        ax.set_ylim([-200,900])
        ax.plot(x[obj], 820 - y[obj], c=color)
    i += 1