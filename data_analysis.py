# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 15:25:08 2017

@author: Syht
"""

from __future__ import division, print_function
import os, glob, math, re, itertools, ast, configparser
import matplotlib.pyplot as plt, numpy as np, pandas as pd
config = configparser.ConfigParser()
config.read('config.ini')
level = config['levels']

df, grad = {}, {}
duration, subjects, levels = [], [], []

# Lecture des fichiers données
for file in glob.glob(os.path.join('..', 'datadir', 'pilot', '*csv')):
    df_ = pd.read_csv(file, '\t')

    _, fname = os.path.split(file)
    fname, ext = fname.split('.')
    date, time, _, level, subj = fname.split('_')

    if subj not in subjects:
        subjects.append(subj)
    if level not in levels:
        levels.append(level)

    try:
        df[subj][level] = {}
        grad[subj][level] = {}
    except:
        df[subj] = {}
        df[subj][level] = {}
        grad[subj] = {}
        grad[subj][level] = {}

    # Création des Dataframes contenant les données afin de pouvoir travailler dessus
    for axis in ['T', 'X', 'Y']:
        for obj in ['gaze', 'ball', 'paddle']:
            df[subj][level][axis+obj] = df_[axis+obj]

    N_start, N_stop = 0, int((df[subj][level]['Tgaze'][len(df[subj][level]['Tgaze'])-1] - df[subj][level]['Tgaze'][0])*30)

    # Détection des changements de signe du gradient
    grad_, t_rebound_, value_old, value_older = [], [], 0, 0
    for k, value in enumerate(np.gradient(df[subj][level]['Yball'])[N_start:N_stop]):   
        # CETTE PARTIE PERMET  DE DETECTER UN REBOND FRAPPANT LA BRIQUE PAR LE BAS
        if value > 0 and  value_older < 0:
            grad_.append(k)
        # CETTE PARTIE PERMET  DE DETECTER UN REBOND FRAPPANT LA BRIQUE PAR LE HAUT
        """if value < 0 and  value_older > 0:
            grad_.append(k)"""
                
        value_older = value_old
        value_old = value

    grad[subj][level] = grad_

lvls_mono = ast.literal_eval(level['lvls_mono'])
lvls_mix = ast.literal_eval(level['lvls_mix'])

# deltav correspond à la fenêtre temporelle centrée sur le rebond dans laquelle vont avoir lieu nos calculs
deltav = 10000
t_mean, lvl, t_sacc, t_rebound, p, t_mean_, lvl_sep, separation_ = {}, {}, {}, {}, {}, [], {}, {}
separation, time, p_, t_rebound_ = {}, {}, {}, {}
for subj in subjects:
    print("Subject: ", subj)
    t_mean[subj], lvl[subj], p[subj], t_sacc[subj], t_rebound[subj], lvl_sep[subj] = [], [], [], [], [], []
    separation[subj], time[subj], separation_[subj], p_[subj], t_rebound_[subj] = {}, {}, [], [], []

    for level in levels:
        separation[subj][level], time[subj][level] = [], []

        print(level)
        lvl_sep[subj].append(df[subj][level]['Tgaze'][len(df[subj][level]['Tgaze'])-1] - df[subj]['lvl1']['Tgaze'][0])
        for v in grad[subj][level]:
            if df[subj][level]['Yball'][v] > 61:
                distance = (df[subj][level]['Ygaze'][v] - df[subj][level]['Yball'][v])**2 + (df[subj][level]['Xgaze'][v] - df[subj][level]['Xball'][v])**2
                distance = np.sqrt(distance)

                distance_ = (df[subj][level]['Ygaze'][v-0] - df[subj][level]['Yball'][v])**2 + (df[subj][level]['Xgaze'][v-0] - df[subj][level]['Xball'][v])**2
                distance_ = np.sqrt(distance_)
                #print(distance_)
                separation[subj][level].append(distance_)
                if subj in ['remi', 'valerie', 'jade', 'thys', 'bruno']:
                    for x, y in itertools.product(range(9), range(11)):
                        if 41+x*139 <= df[subj][level]['Xball'][v] < 180+x*139 and 38+y*45 <= df[subj][level]['Yball'][v] < 83+y*45:
                            p_[subj].append(lvls_mono[int(re.findall(r'\d+', level)[0]) - 1][y][x])
                            t_rebound_[subj].append(df[subj][level]['Tgaze'][v])
                            separation_[subj].append(distance_)

                time[subj][level].append(df[subj][level]['Tgaze'][v]-df[subj][level]['Tgaze'][0])

                if distance < 200:
                    i = v-1
                    dist = (df[subj][level]['Ygaze'][v:v+deltav] - df[subj][level]['Yball'][v])**2 + (df[subj][level]['Xgaze'][v:v+deltav] - df[subj][level]['Xball'][v])**2
                    dist = np.sqrt(dist)
                    derivate = np.diff(dist)
                    if len(dist) != len(derivate):
                        derivate = np.append(derivate, np.nan)
                    for d in dist:
                        i += 1
                        if derivate[i-v] > 30:
                            print(df[subj][level]['Xball'][v], df[subj][level]['Yball'][v])
                            
                            """Niveaux Mixtes"""
                            if subj in ['juliette', 'elisa', 'maxime']:
                                for x, y in itertools.product(range(9), range(9)):
                                    if 41+x*139 <= df[subj][level]['Xball'][v] < 180+x*139 and 38+y*45 <= df[subj][level]['Yball'][v] < 83+y*45:
                                        p[subj].append(lvls_mix[int(re.findall(r'\d+', level)[0]) - 1][y][x])
                                        t_sacc[subj].append(df[subj][level]['Tgaze'][i]-df[subj][level]['Tgaze'][v])
                                        #print(lvls_mix[int(re.findall(r'\d+', level)[0]) - 1][y][x])
                                        t_rebound[subj].append(df[subj][level]['Tgaze'][v])

                            """Niveaux Monochromatiques"""
                            if subj in ['remi', 'valerie', 'jade', 'thys', 'bruno']:
                                for x, y in itertools.product(range(9), range(11)):
                                    if 41+x*139 <= df[subj][level]['Xball'][v] < 180+x*139 and 38+y*45 <= df[subj][level]['Yball'][v] < 83+y*45:
                                        p[subj].append(lvls_mono[int(re.findall(r'\d+', level)[0]) - 1][y][x])
                                        t_sacc[subj].append(df[subj][level]['Tgaze'][i]-df[subj][level]['Tgaze'][v])
                                        print(lvls_mono[int(re.findall(r'\d+', level)[0]) - 1][y][x])
                                        t_rebound[subj].append(df[subj][level]['Tgaze'][v])
                            break

        if np.std(t_sacc[subj]) < 10/10*np.mean(t_sacc[subj]):
            t_mean[subj].append(np.mean(t_sacc[subj]))
            t_mean_.append(np.mean(t_sacc[subj]))
            lvl[subj].append(re.findall(r'\d+', level)[0])
            print(np.mean(t_sacc[subj]), '+/-', np.std(t_sacc[subj]))

print(lvl)

for subj in subjects:
    for level in levels:
        # Sujets considérés
        if subj in ['remi', 'valerie', 'jade', 'thys', 'bruno']:
            fig, ax = plt.subplots(figsize=(15,8))
            ax.plot(time[subj][level], separation[subj][level], 'bo-')
            ax.set_title('Subject: ' + subj + ' ' + level)
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Distance rebound/gaze (pixels)')

for subj in subjects:
    # Sujets considérés
    if subj in ['remi', 'valerie', 'jade', 'thys', 'bruno']:
        fig, ax = plt.subplots(figsize=(15,8))
        ax.scatter(t_rebound_[subj]-t_rebound_[subj][0], separation_[subj], c=p_[subj], s=100, cmap='plasma_r')
        for sep in lvl_sep[subj]:
            ax.plot([sep, sep], [0, 1200], 'k--')
        ax.set_title('Subject: ' + subj)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Distance rebound/gaze (pixel)')

for subj in subjects:
    # Sujets considérés
    if subj in ['remi', 'valerie', 'jade', 'thys', 'bruno']:
        fig, ax = plt.subplots(figsize=(15,8))
        ax.scatter(t_rebound[subj]-t_rebound[subj][0], t_sacc[subj], c=p[subj], s=100, cmap='plasma_r')
        for sep in lvl_sep[subj]:
            ax.plot([sep, sep], [0, 1.75], 'k--')
        ax.set_title('Subject: ' + subj)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Latency (s)')

for subj in subjects:
    fig, ax = plt.subplots(figsize=(15,8))
    ax.scatter(lvl[subj], t_mean[subj])
    ax.set_title('Subject: ' + subj)
    ax.set_xlabel('Levels')
    ax.set_ylabel('Latency (s)')
    ax.set_xlim(0, 7)