import os, matplotlib.pyplot as plt, numpy as np, pandas as pd

time, x, y = {}, {}, {}

datadir, tagg, subject = 'datadir', '2017-06-28_144217', 'juliette'
tags = ['2017-06-28_133727', '2017-06-28_134443', '2017-06-28_135020', '2017-06-28_135706', '2017-06-28_140322', '2017-06-28_141025']
fig = ['fig1', 'fig2', 'fig3', 'fig4', 'fig5', 'fig6']


i = 0
for tag in tags:
    fig[i], ax = plt.subplots(figsize=(15,8))
    df = pd.read_csv(os.path.join(datadir, 'pilot', tag + '_dataframe_lvl'+ str(i+1) + '_' + subject + '.csv'), '\t')

    for obj, color in zip(['gaze', 'ball', 'paddle'], ['g', 'b', 'r']):
        if obj == 'gaze':
            time[obj], x[obj], y[obj] = df.loc[:,'Tgaze'], df.loc[:,'Xgaze'], df.loc[:,'Ygaze']
        if obj == 'ball':
            time[obj], x[obj], y[obj] = df.loc[:,'Tball'], df.loc[:,'Xball'], df.loc[:,'Yball']
        if obj == 'paddle':
            time[obj], x[obj], y[obj] = df.loc[:,'Tpaddle'], df.loc[:,'Xpaddle'], df.loc[:,'Ypaddle']
        ax.set_xlim([-100,1400])
        ax.set_ylim([-100,1100])
        ax.set_ylim(ax.get_ylim()[::-1]) # invert the y-axis
        ax.plot(x[obj], y[obj], c=color)
    i += 1