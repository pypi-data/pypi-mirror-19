# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 05:03:19 2017

@author: dawkiny
"""

from pandas import DataFrame as df
import os
from os.path import dirname, abspath


def datalist():

    filepath = dirname(abspath(__file__))
    print(os.listdir(filepath))


def load(filename):

    data = _get_data(filename)

    return data


def _get_data(filename):

    filepath = dirname(abspath(__file__))
    file = filepath + '/{}/{}.data'.format(filename, filename)
    data = df.read_csv(open(file, 'rb'), sep=",")

    return data
