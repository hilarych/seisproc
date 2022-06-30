#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions for FK domain 2D seismic data processing. 

The script is distributed under the terms of the GNU General Public License as 
published by the Free Software Foundation (version 3 or later version).

@author: Hilary Chang

"""

import numpy as np
from scipy.ndimage import gaussian_filter
import scipy.fftpack as sfft
import matplotlib.pyplot as plt


def fk_filter(data_fft2,fst,fsx, vmax=10000,vmin=0,
              filt_downgoing=False,filt_upgoing=False,
              smooth=5):
    '''
    Given data in the FK domain, filter data with desired velocity range and directions, 
    and return the filtered data in the time domain.
    '''
    Nx, Nt = data_fft2.shape

    # Initialize
    mask = np.ones(shape=data_fft2.shape)
    
    for k in range(1,int(Nx/2)):
        for w in range(1,int(Nt/2)):
            v = (w*fst/Nt)/(k*fsx/Nx) 
            print('Resolution:\n df = %s Hz\n dk = %s m^-1'%(fst/Nt,fsx/Nx))
            # Note: resolution is  dw=fst/Nt and dk=fsx/Nx
            # Note that dk and dw here have unit m^(-1) and s^(-1). ie. They are 
            # actually k/(2pi) and f=w/(2pi) in common notation.
            
            if filt_downgoing == True:
                mask[-k][w]= 0  # lower left quadrant
                mask[k][-w]= 0  # upper right quadrant
            if filt_upgoing == True:
                mask[k][w]= 0   # upper left quadrant
                mask[-k][-w]= 0 # lower right quadrant
            if vmax!=None and v >= vmax:
                mask[k][w]= 0   # upper left quadrant
                mask[k][-w]= 0  # upper right quadrant
                mask[-k][w]= 0  # lower left quadrant
                mask[-k][-w]= 0 # lower right quadrant
            if vmin!=None and v <= vmin:
                mask[k][w]= 0   # upper left quadrant
                mask[k][-w]= 0  # upper right quadrant
                mask[-k][w]= 0  # lower left quadrant
                mask[-k][-w]= 0 # lower right quadrant
    
    # Smooth the filter
    mask= gaussian_filter(mask,sigma=smooth,mode='wrap')
    
    # Apply the filter 
    data_filt= sfft.ifft2(data_fft2*mask).real

    # Quick plots to check results 
    # plot_fk_domain(f=ff,k=kk,c=np.abs(data_fft2),
    #                  fst=fst,fsx=fsx,vm=2)
    # plot_fk_domain(f=ff,k=kk,c=mask,
    #                  fst=fst,fsx=fsx,vm=0)

    return data_filt, mask   


def plot_fk_domain(f,k,c,fst,fsx,vm=0,figsize=(6,3)):
    '''
    Plot shifted fk domain image given unshifted data and axis (eg. generated 
    using scipy.fft.fftfreq and scipy.fft.fft.

    Parameters
    ----------
    f : numpy 1D array
        Frequency axis from scipy.fftpack.fftfreq.
    k : numpy 1D array
        Wave number axis from scipy.fftpack.fftfreq.
    c : numpy 2D array
        Any data with from scipy.fftpack.fft2 with shape shape (len(k), len(f)).
    fst : TYPE
        DESCRIPTION.
    fsx : TYPE
        DESCRIPTION.
    vm : float, optional
        Colorbar scale (range: 0-100). 
        eg. 0: display all color range. 10: exclude highest & lowest 10% data.
        The default is 0.
    figsize : tuple, optional
        The default is (6,3).

    Returns
    -------
    ax : matplotlib.axes
        An FK domain plot ax.

    '''
    Nx, Nt = c.shape
    k   = sfft.fftfreq(Nx, d=1/fsx)
    f   = sfft.fftfreq(Nt, d=1/fst)
    vm1 = np.percentile(c, 0+vm)
    vm2 = np.percentile(c, 100-vm)
    fig,ax=plt.subplots(figsize=figsize)
    qmesh = ax.pcolorfast(
                            sfft.fftshift(f), sfft.fftshift(k),
                            sfft.fftshift(c),
                            vmin=vm1, vmax=vm2, cmap='Blues'
                            )
    cbar=plt.colorbar(qmesh)
    cbar.set_label('Amplitude')
    plt.axvline(x=0,ls='--',lw=0.5,color='r')
    plt.axhline(y=0,ls='--',lw=0.5,color='r')
    plt.ylabel(r'$f_x$ ($m^{-1}$)')
    plt.xlabel(r'$f_t$ ($s^{-1}$)')
    plt.title(r'$N_t={0:d},\ f_{{st}}={1:f} Hz,\ N_x={2:d},\ f_{{sx}}={3}\ /m$'.format(
        Nt,fst,Nx,fsx))
    plt.tight_layout()
    plt.show
    return ax

