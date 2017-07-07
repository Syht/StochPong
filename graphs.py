import os, matplotlib.pyplot as plt, numpy as np, pandas as pd, math

time, x, y = {}, {}, {}

datadir, tagg, subject = 'datadir', '2017-06-28_144217', 'jade'
tags = ['2017-07-06_141752', '2017-07-06_142006', '2017-07-06_142210', '2017-07-06_142445', '2017-07-06_142843', '2017-07-06_143208']
fig = ['fig1', 'fig2', 'fig3', 'fig4', 'fig5', 'fig6']


i = 0
for tag in tags:
    fig[i], ax = plt.subplots(figsize=(15,8))
    df = pd.read_csv(os.path.join(datadir, tag + '_dataframe_lvl'+ str(i+1) + '_' + subject + '.csv'), '\t')

    for obj, color in zip(['gaze', 'ball', 'paddle'], ['g', 'b', 'r']):
        if obj == 'gaze':
            time[obj], x[obj], y[obj] = df.loc[:,'Tgaze'], df.loc[:,'Xgaze'], df.loc[:,'Ygaze']
        if obj == 'ball':
            time[obj], x[obj], y[obj] = df.loc[:,'Tball'], df.loc[:,'Xball'], df.loc[:,'Yball']
        if obj == 'paddle':
            time[obj], x[obj], y[obj] = df.loc[:,'Tpaddle'], df.loc[:,'Xpaddle'], df.loc[:,'Ypaddle']
        
        ax.set_xlim([-10,1300])
        ax.set_ylim([-10,1000])
        ax.set_ylim(ax.get_ylim()[::-1]) # invert the y-axis
        ax.plot(x[obj], y[obj], c=color)

    #dt = time['gaze'] - time['ball']
    #print('mean', dt.mean, ' +/- ', dt.std)

    """ First line: plot time(Xgaze) | Second line: plot time(Ygaze) """
    """plt.plot(time['gaze']-time['gaze'][0], x['gaze'])
    plt.plot(time['gaze']-time['gaze'][0], y['gaze'])"""
    
    """N_start, N_stop = 60, 140
    plt.plot(time['gaze'][N_start:N_stop]-time['gaze'][0], np.gradient(y['gaze'])[N_start:N_stop])
    N_start, N_stop = 55, 130
    plt.plot(time['ball'][N_start:N_stop]-next(x for x in time['ball'] if not math.isnan(x)), np.gradient(y['ball'])[N_start:N_stop], c='r')"""
    i += 1