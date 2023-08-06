#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 20:55:26 2017

@author: dawkiny
"""

from pydawkiny.manufacture.Lot import wafer, displaypanel

#%% wafer

# Create a wafer
alot = wafer(fac_id='Factory1', lot_cd='ABC', end_tm='20161101123456',
             size=(50, 30), unit_cnt=20, pattern=['P', 'F'], p=[.7, .3])

# Check it
alot.groupby(['unit_id', 'val'])['end_tm'].count()
len(alot[alot.unit_id == '01'])

# Visualize it
aplt = wafer.unitplot(alot, columns=['xcoord', 'ycoord'],
                      lot_id='', unit_id='02', val='val', figsize=(12, 9),
                      pattern=['F'], m=['s'], s=[50], c=['red'],
                      a=[.5], shown='y')

# Show it
aplt.show()

# Others
len(alot.groupby('unit_id').groups)
len(alot.groupby('unit_id').groups.items())
alot.groupby('unit_id').groups
alot.groupby('unit_id').groups.items()
alot.groupby('unit_id')['val']


#%% displaypanel

# Create a displaypanel
blot = displaypanel(fac_id='Factory2', lot_cd='BBC', end_tm='20161101123456',
                    size=(60, 20), unit_cnt=5,
                    pattern=['P', 'B', 'F'], p=[.8, 0.15, .05])

# Check it
blot.groupby(['unit_id', 'val'])['end_tm'].count()
len(blot[blot.unit_id == '01'])

# Visualize it
bplt = displaypanel.unitplot(blot, columns=['xcoord', 'ycoord'],
                             lot_id='', unit_id='02', pattern=['B', 'F'],
                             val='val', m=['s', 'o'], s=[50, 50],
                             c=['red', 'blue'], a=[.5, .5], shown='n')

# Show it
bplt.show()


#%% VIF

import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor as stats_vif

tmp = pd.read_csv('/media/dawkiny/M/BigData/Datasets/wine/winequality-white.csv', sep=',')
tmp.to_csv('/media/dawkiny/M/BigData/Datasets/wine/wine.data', sep=',', header=True, index=False)
tmp.shape


col = tmp.columns
col



tmp_y = tmp.ix[:, 0]
tmp_x = tmp.ix[:, list(range(1, len(tmp.columns)))]

tmp_x.shape
tmp_y.shape

#%%
tmp.values[:,0]
stats_vif(tmp.values, 0)

res = vif(tmp, thresh=5.0)
#%%

def vif(data, thresh=5.0):

    dropped = True
    while dropped == True :
        variables = list(range(data.shape[1]))
        dropped = False
		
        vifTable = [stats_vif(data[variables].values, col) for col in range(data[variables].shape[1])]

        maxLoc = vifTable.index(max(vifTable))

        if max(vifTable) >= thresh:

            print('Dropping \'' + data[variables].columns[maxLoc] + '\' at index: ' + str(maxLoc))

            data = data.drop(data.columns[maxLoc], axis=1)
            del variables[maxLoc]

            dropped = True

    print('Remaining Variables')
    print(data.columns[variables])

    return data[variables]

#%% scipy

import scipy as sp
sp.stats.linregress(x, y=None)[source]


#%% sklearn
import numpy as np
from sklearn.linear_model import LinearRegression

tmp_x[:, np.newaxis]
tmp_x.values

lr = LinearRegression()
xx = lr.fit(tmp_y, tmp_x[:, np.newaxis])

xx = lr.fit(tmp_x[:, np.newaxis], tmp_y)

#%%

import numpy as np
import statsmodels.api as sm

def reg_m(y, x):
    ones = np.ones(len(x[0]))
    X = sm.add_constant(np.column_stack((x[0], ones)))
    for ele in x[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    results = sm.OLS(y, X).fit()
    return results

print(reg_m(tmp_y, tmp_x).summary())


## fit a OLS model with intercept on TV and Radio
reg_x = sm.add_constant(tmp_x)
est = sm.OLS(tmp_y, reg_x).fit()
est.rsquared
est.summary()

#%%
from statsmodels.stats.outliers_influence import variance_inflation_factor as stats_vif
tmp.as_matrix()
tmp.values
stats_vif(tmp.values, 0)

tmp.columns[list(range(1, tmp.shape[1]))]

tmp[tmp.columns[list(range(1, tmp.shape[1]))]]
