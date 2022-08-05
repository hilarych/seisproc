#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

A collection of useful functions for seismic data processing. 

The scripts are distributed under the terms of the GNU General Public License as 
published by the Free Software Foundation (version 3 or later version).

@author: Hilary Chang

"""
from scipy.signal import hann,wiener
import numpy as np
import scipy
from time import time
import scipy.fftpack as sfft

def opt_fft(data):
    '''
    perform fft with optimized array length.
    data: 2D array (nx, nt) or 1D array (nt)
    
    Modified from code by Hongrui Qiu.
    
    '''
    nmin = data.shape[-1]*2
    nopt = sfft.next_fast_len(nmin)
    spec = sfft.fft(data,n=nopt)
    return spec


def guassian_BPF(wf,f,dt,alpha=20):
    '''
    Narrow bandpass filter using a Gaussian function.
    alpha - width of the bandpass
    per - Center periods of the bandpass
    
    return:
    Complex 1D array (ns) 
        
    '''
    sf = opt_fft(wf) # data spectrum in the f domain
    ns = len(sf)       # Number of sample (time)
    dom = 2*np.pi/ns/dt
    om = 2*np.pi*f
    b = np.exp(-((dom*np.arange(ns)-om)/om)**2*alpha)

    fils = b*sf
    # fill with zeros half spectra for Hilbert transformation and
    # spectra ends ajustment
    for m in range(ns//2+1,ns,1):
        fils[m] = 0.0
    fils[0] /= 2.0
    fils[ns//2] = np.real(fils[ns//2])
    # forward FFT: fils ==> tmp
    tmp = sfft.ifft(fils)
    return tmp[0:ns]



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


def one_side_2_both_sides(st):
    
    for k,tr in enumerate(st): 
        data_pos= tr.data
        data_neg=data_pos[1:]
        data =np.concatenate((data_neg[::-1],data_pos))
        st[k].data= data

        t0=tr.stats.sac.t0+ len(data_neg)/tr.stats.sampling_rate
        st[k].stats.sac['t0']=t0

    return st 


def NCF_denoising(img_to_denoise,Mdate,Ntau,NSV):
    '''
    SVDWF method from Moreau et al (2017)
    Inputs:
        - img_to_denoise: the list of NCF. It should be an MxN matrix where M 
            represents the total number of NCF and N the
            length of each NCF
        - mdate: the size of the Wiener filter in the first dimension (K = 5)
        - ntau: the size of the Wiener filter in the second dimension (L = 5)
        - nsv: the number of singular values to keep in the SVD filter (25)
    Outputs:
        - denoised_img: the denoised list of NCF
    
    '''
    t1 = time()
    if img_to_denoise.ndim ==2:
        M,N = img_to_denoise.shape
        if NSV > np.min([M,N]):
            NSV = np.min([M,N])
        [U,S,V] = scipy.linalg.svd(img_to_denoise,full_matrices=False)
        print ('SVD done, time used',time()-t1)
        S = scipy.linalg.diagsvd(S,S.shape[0],S.shape[0])
        print (time()-t1)
        Xwiener = np.zeros([M,N])
        for kk in range(NSV):
            str_out = '%d/%d, total time used %.2fs' % (kk,NSV,time()-t1)
            print (str_out)
            SV = np.zeros(S.shape)
            SV[kk,kk] = S[kk,kk]
            X = U@SV@V
            Xwiener += wiener(X,[Mdate,Ntau])
            
        denoised_img = wiener(Xwiener,[Mdate,Ntau])
    elif img_to_denoise.ndim ==1:
        M = img_to_denoise.shape[0]
        NSV = np.min([M,NSV])
        denoised_img = wiener(img_to_denoise,Ntau)
        temp = np.trapz(np.abs(np.mean(denoised_img) - img_to_denoise))    
        denoised_img = wiener(img_to_denoise,Ntau,np.mean(temp))

    return denoised_img