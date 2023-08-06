# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 03:46:03 2017

@author: dawkiny
"""

import pandas as pd
import statsmodels.api as sm


def vif(y, X):

    assert isinstance(y, pd.Series)
    assert isinstance(X, pd.DataFrame)

    # Change input to array
    y_arr = y.values
    X_arr = X.values

    # Calculate a linear regression(Ordinary Least Square)
    reg = sm.add_constant(X_arr)
    est = sm.OLS(y_arr, reg).fit()

    # Get a R-square
    rsq = est.rsquared

    # Get a VIF
    vif = 1 / (1 - rsq)

    print(vif)

    return vif


def feature_selection_vif(data, thresh=.5):

    assert isinstance(data, pd.DataFrame)

    # Create Dropped variable list
    dropped = pd.DataFrame(columns=['var', 'vif'])

    # Startswith 'drop = True'(Assume that some variables will be dropped)
    dropCondition = True

    # Calculate a VIF & Drop columns(variables)
    while dropCondition:

        # 1. Calculate a VIF
        vifList = [vif(data.loc[:, col], data.loc[:, data.columns != col])
                   for col in data.columns]

        # Get the MAXIMUM VIF
        max_val = max(vifList)
        max_idx = vifList.index(max(vifList))
        max_var = data.columns[max_idx]

        # 2. IF VIF values are over the threshold, THEN drop it
        if max_val >= thresh:

            # Keep it
            dropped = dropped.append({'var': max_var, 'vif': max_val},
                                     ignore_index=True)

            # Drop it
            data = data.drop(data.columns[max_idx], axis=1)

            # Print it
            print("Dropping '" + str(data.columns[max_idx]) + "'" +
                  "at index: " + str(max_idx) +
                  "\n VIF: " + str(max_val))

            # Since a variable has been dropped, the assumption remains
            dropCondition = True

        else:

            # No variable dropped, the assumption has been rejected
            dropCondition = False

    print('Remaining Variables')
    print(data.columns)

    return data, dropped
