#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 23:18:27 2017

@author: dawkiny
"""

import numpy as np
import pandas as pd
from pandas import DataFrame as df
from datetime import datetime as dt
import itertools as it
import random, string
import matplotlib.pyplot as plt

###########################
fab_id='M14'
lot_cd='TCC'
alias_lot_id='TCCK108'
wf_id=list(range(1, 26))
end_tm = '20161101180025'
size=(40, 30)
############################

# Create Wafer DataFrame
def create(fab_id=None, lot_cd=None, end_tm=None, size=(None, None)):
    
    xsize, ysize = size
    
    wafer = df(columns=['fab_id', 'lot_cd', 'alias_lot_id', 'wf_id',
                        'end_dt', 'end_tm', 'xcoord', 'ycoord', 'res_val'],
               index=range(0, xsize * ysize * 25))
    
    # Import values to each Field
    
    ## fab_id, lot_cd
    wafer.fab_id, wafer.lot_cd = fab_id, lot_cd
    
    ## alias_lot_id
    id1 = ''.join([random.choice(string.ascii_uppercase + string.digits) for n in range(1)])
    id2 = ''.join([random.choice(string.digits) for n in range(3)])
    wafer.alias_lot_id = lot_cd + id1 + id2
    
    ## wf_id
    wf_iter = [list(it.repeat(wf_num, xsize * ysize)) for wf_num in range(1, 26)]
    wafer.wf_id = list(it.chain.from_iterable(wf_iter))
    wafer.wf_id = wafer.wf_id.astype(str).str.zfill(2)
    
    ## end_tm, end_dt
    wafer.end_tm = dt.strptime(end_tm, '%Y%m%d%H%M%S')
    wafer.end_dt = end_tm.date()
    
    ## x_coordinate, y_coordinate
    coords = tuple(it.product(list(range(1, xsize+1)), list(range(1, ysize+1)) ))
    wafer.xcoord, wafer.ycoord = zip(*coords*25)
    
    ## res_val
    wafer.res_val = np.random.choice(list(string.ascii_uppercase[0:20]), wafer.shape[0])
    
    print('-'*25)
    print('ALIAS_LOT_ID : ' + lot_cd + id1 + id2)
    print('-'*25)
    return wafer
    


# Wafer Visualization
def plot():
    plt.figure(figsize=(12, 9))
    plt.scatter(wafer.xcoord, wafer.ycoord, marker='+', s=1000, c='grey', alpha=.1)
    plt.scatter(wafer.xcoord[wafer.res_val=='A'], wafer.ycoord[wafer.res_val=='A'], marker='s', s=100, c='red', alpha=.5)
    