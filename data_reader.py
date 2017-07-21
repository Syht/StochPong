# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 11:08:29 2017

@author: Syht
"""

import os, glob, pandas as pd

def data_reader():
    df = {}

    for file in glob.glob(os.path.join('..', 'datadir', 'pilot', '*csv')):
        df_ = pd.read_csv(file, '\t')

        _, fname = os.path.split(file)
        fname, ext = fname.split('.')
        date, time, _, level, subj = fname.split('_')

        try:
            df[subj][level] = {}
        except:
            df[subj] = {}
            df[subj][level] = {}

        for axis in ['T', 'X', 'Y']:
            for obj in ['gaze', 'ball', 'paddle']:
                df[subj][level][axis+obj] = df_[axis+obj]
    return df