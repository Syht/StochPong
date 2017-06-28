# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 15:25:27 2017

@author: Syht
"""

import pandas as pd, os, numpy as np

datadir, tag, subject = 'datadir', '2017-06-28_142510', 'remi'    

gazefile = open(os.path.join(datadir, tag + '_gaze_' + subject + '.txt'), "r")
ballfile = open(os.path.join(datadir, tag + '_ball_' + subject + '.txt'), "r")
paddlefile = open(os.path.join(datadir, tag + '_paddle_' + subject + '.txt'), "r")

glines = gazefile.readlines()
blines = ballfile.readlines()
plines = paddlefile.readlines()

gazefile.close()
ballfile.close()
paddlefile.close()

Tgaze = []
Xgaze = []
Ygaze = []
GazeState = []
Tball = []
Xball = []
Yball = []
Tpaddle = []
Xpaddle = []
Ypaddle = []

for x in glines:
    if x.split(';')[4] == '..PEG':
        Tgaze.append(x.split(';')[2])
        GazeState.append(x.split(';')[4])
        Xgaze.append(x.split(';')[5])
        Ygaze.append(x.split(';')[6])
    else:
        Tgaze.append(x.split(';')[2])
        GazeState.append(x.split(';')[4])
        Xgaze.append(np.nan)
        Ygaze.append(np.nan)

for x in blines:
    Tball.append(str(int(x.split(';')[0])/1000))
    Xball.append(x.split(';')[1])
    Yball.append(x.split(';')[2].replace('\n',''))

for x in plines:
    Tpaddle.append(str(int(x.split(';')[0])/1000))
    Xpaddle.append(x.split(';')[1])
    Ypaddle.append(x.split(';')[2].replace('\n',''))

if len(glines) > len(blines):
    Tball = np.hstack((np.zeros(len(Tgaze)-len(Tball)) + np.nan, Tball))
    Xball = np.hstack((np.zeros(len(Xgaze)-len(Xball)) + np.nan, Xball))
    Yball = np.hstack((np.zeros(len(Ygaze)-len(Yball)) + np.nan, Yball))

if len(plines) - len(glines) == 1:
    Tpaddle = np.delete(Tpaddle, 0)
    Xpaddle = np.delete(Xpaddle, 0)
    Ypaddle = np.delete(Ypaddle, 0)

datasheet = pd.DataFrame(
        {'Tgaze' : Tgaze, 'Xgaze' : Xgaze, 'Ygaze' : Ygaze, 'GazeState' : GazeState,
         'Tball' : Tball, 'Xball' : Xball, 'Yball' : Yball,
         'Tpaddle' : Tpaddle, 'Xpaddle' : Xpaddle, 'Ypaddle' : Ypaddle})

pd.set_option('display.width', 160)
pd.set_option('display.max_rows', len(datasheet))
datasheet = datasheet[['GazeState', 'Tgaze', 'Xgaze', 'Ygaze', 'Tball', 'Xball', 'Yball', 'Tpaddle', 'Xpaddle', 'Ypaddle']]
datasheet.to_csv(os.path.join('datadir', tag + '_dataframe_' + subject + '.csv'), sep='\t')
with open(os.path.join('datadir', tag + '_dataframe_' + subject + '.df'), 'w') as data:
    data.write('%s' %datasheet)
