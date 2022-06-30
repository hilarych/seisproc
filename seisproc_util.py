#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

A collection of useful functions for seismic data processing. 

The scripts are distributed under the terms of the GNU General Public License as 
published by the Free Software Foundation (version 3 or later version).

@author: Hilary Chang

"""
from scipy.signal import hann
import numpy as np


def hann_taper(data,percentage=0.1,wlen=None,left_right='both'):
    '''
    Taper the edges of the 2d array data on the last axis. 
    Default: Taper length based on percentage of total points unless wlen is 
    specified. 
    
    Parameters
    ----------
    data : numpy 2D array
        Data shape: (m traces, n time sample)
    percentage : float, optional
        Only used when wlen==None. Taper length at the edges based on percentage 
        of total points. The default is 0.1.
    wlen : int, optional
        Taper length at the edges in samples. The default is None.
    left_right : str, optional
        Which edge to taper. 
        Options: "both", "left", "right"
        The default is 'both'.

    Returns
    -------
    data_tapered : numpy 2D array
        Data tapered along the last axis.

    '''
    
    npts = np.size(data,-1)  # Default: Apply taper to the last dimension
    
    if wlen == None:
        wlen = int(round(npts*percentage))
    
    window = hann(wlen*2)
    if left_right=='both':
        left = window[:wlen]
        right = window[wlen:]
    elif left_right=='left':
        left = window[:wlen]
        right = np.ones(wlen)
    elif left_right=='right':
        left = np.ones(wlen)
        right = window[wlen:]
    else:
        raise Exception('Available options for left_right: "both", "left", "right"')
        
    middle = np.ones(int(npts-wlen*2))
    window = np.concatenate((left, middle, right))
    data_tapered = data* window
    
    return data_tapered