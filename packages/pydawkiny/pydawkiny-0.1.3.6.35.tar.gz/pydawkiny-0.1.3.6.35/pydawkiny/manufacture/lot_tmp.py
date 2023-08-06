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

import math
from pydawkiny.geometry import Ellipse


class lot:
    
    # Create lotData DataFrame
    def __init__(self, fab_id=None, lot_cd=None, end_tm=None, size=None):

        assert len(size) == 2
        self.fab_id = fab_id
        self.lot_cd = lot_cd
        self.end_tm = end_tm
        self.size = size
        
    def __new__(cls, fab_id=None, lot_cd=None, end_tm=None, size=None):
        
        coords = Ellipse(size).coordinates()
        xsize, ysize = coords.xcoord.max(), coords.ycoord.max()
        
        lotData = df(columns=['fab_id', 'lot_cd', 'alias_lot_id', 'wf_id',
                            'end_dt', 'end_tm', 'xcoord', 'ycoord', 'res_val'],
                   index=range(0, coords.shape[0] * 25))

        # Import values to each Field
        
        ## fab_id, lot_cd
        lotData.fab_id, lotData.lot_cd = fab_id, lot_cd
        
        ## alias_lot_id
        id1 = ''.join([random.choice(string.ascii_uppercase + string.digits) for n in range(1)])
        id2 = ''.join([random.choice(string.digits) for n in range(3)])
        lotData.alias_lot_id = lot_cd + id1 + id2
        
        ## wf_id
        lotIter = [list(it.repeat(wf_num, len(coords))) for wf_num in range(1, 26)]
        lotData.wf_id = list(it.chain.from_iterable(lotIter))
        lotData.wf_id = lotData.wf_id.astype(str).str.zfill(2)
        
        ## end_tm, end_dt
        lotData.end_tm = dt.strptime(end_tm, '%Y%m%d%H%M%S')
        lotData.end_dt = lotData.end_tm.map(lambda x: x.date())
        
        ## x_coordinate, y_coordinate
        lotData.xcoord = list(coords.xcoord) * 25
        lotData.ycoord = list(coords.ycoord) * 25
        
        ## res_val
        lotData.res_val = np.random.choice(list(string.ascii_uppercase[0:20]), lotData.shape[0])
        
        print('-'*25)
        print('ALIAS_LOT_ID : ' + lot_cd + id1 + id2)
        print('-'*25)
        return lotData
        
        
        return super().__new__(cls)
        
    def create(self):

        coords = Ellipse(self.size).coordinates()
        xsize, ysize = coords.xcoord.max(), coords.ycoord.max()
        
        lotData = df(columns=['fab_id', 'lot_cd', 'alias_lot_id', 'wf_id',
                            'end_dt', 'end_tm', 'xcoord', 'ycoord', 'res_val'],
                   index=range(0, coords.shape[0] * 25))

        # Import values to each Field
        
        ## fab_id, lot_cd
        lotData.fab_id, lotData.lot_cd = self.fab_id, self.lot_cd
        
        ## alias_lot_id
        id1 = ''.join([random.choice(string.ascii_uppercase + string.digits) for n in range(1)])
        id2 = ''.join([random.choice(string.digits) for n in range(3)])
        lotData.alias_lot_id = self.lot_cd + id1 + id2
        
        ## wf_id
        lotIter = [list(it.repeat(wf_num, len(coords))) for wf_num in range(1, 26)]
        lotData.wf_id = list(it.chain.from_iterable(lotIter))
        lotData.wf_id = lotData.wf_id.astype(str).str.zfill(2)
        
        ## end_tm, end_dt
        lotData.end_tm = dt.strptime(self.end_tm, '%Y%m%d%H%M%S')
        lotData.end_dt = lotData.end_tm.map(lambda x: x.date())
        
        ## x_coordinate, y_coordinate
        lotData.xcoord = list(coords.xcoord) * 25
        lotData.ycoord = list(coords.ycoord) * 25
        
        ## res_val
        lotData.res_val = np.random.choice(list(string.ascii_uppercase[0:20]), lotData.shape[0])
        
        print('-'*25)
        print('ALIAS_LOT_ID : ' + self.lot_cd + id1 + id2)
        print('-'*25)
        return lotData

        
    # lotData Visualization
    def wfplot(data, columns=['xcoord', 'ycoord'], wfid=None, figsize=None, bad=None, m=('+', 's'), s=(1000, 100), c=('grey', 'red'), a=(.1, .5), shown=None):
        
        assert len(figsize) == 2
        assert len(columns) == 2
        assert isinstance(wfid, str) == True
        assert len(wfid) == 2
        
        if shown == 'y':
            
            if wfid != None:

                pltData = data[data.wf_id==wfid]
            
                fig = plt.figure(figsize=figsize)
                plt.scatter(pltData.xcoord, pltData.ycoord, marker=m[0], s=s[0], c=c[0], alpha=a[0])
                plt.scatter(pltData.xcoord[pltData.res_val==bad],
                            pltData.ycoord[pltData.res_val==bad], marker=m[1], s=s[1], c=c[1], alpha=a[1])
                fig.suptitle(str(pltData.alias_lot_id.unique() + pltData.wf_id.unique()))
                #fig.tight_layout()
    
            else:
    
                pltData = data
                pltData.xcoord = pltData[columns[0]]
                pltData.ycoord = pltData[columns[1]]
            
                fig = plt.figure(figsize=figsize)
                plt.scatter(pltData.xcoord, pltData.ycoord, marker=m[0], s=s[0], c=c[0], alpha=a[0])
                plt.scatter(pltData.xcoord[pltData.res_val==bad],
                            pltData.ycoord[pltData.res_val==bad], marker=m[1], s=s[1], c=c[1], alpha=a[1])
                fig.suptitle(str(pltData.alias_lot_id.unique() + pltData.wf_id.unique()))
                #fig.tight_layout()
        
    elif shown == 'n':
        
        if wfid != None:

            pltData = data[data.wf_id==wfid]
        
            fig = plt.figure(figsize=figsize)
            fig.scatter(pltData.xcoord, pltData.ycoord, marker=m[0], s=s[0], c=c[0], alpha=a[0])
            fig.scatter(pltData.xcoord[pltData.res_val==bad],
                        pltData.ycoord[pltData.res_val==bad], marker=m[1], s=s[1], c=c[1], alpha=a[1])
            fig.suptitle(str(pltData.alias_lot_id.unique() + pltData.wf_id.unique()))
            #fig.tight_layout()

        else:

            pltData = data
            pltData.xcoord = pltData[columns[0]]
            pltData.ycoord = pltData[columns[1]]
        
            fig = plt.figure(figsize=figsize)
            fig.scatter(pltData.xcoord, pltData.ycoord, marker=m[0], s=s[0], c=c[0], alpha=a[0])
            fig.scatter(pltData.xcoord[pltData.res_val==bad],
                        pltData.ycoord[pltData.res_val==bad], marker=m[1], s=s[1], c=c[1], alpha=a[1])
            fig.suptitle(str(pltData.alias_lot_id.unique() + pltData.wf_id.unique()))
            #fig.tight_layout()

        
        return fig
        
