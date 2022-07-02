#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Function for visualization. 

The scripts are distributed under the terms of the GNU General Public License as 
published by the Free Software Foundation (version 3 or later version).

@author: Hilary Chang
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def plot_sta_groups_map(plot_sta_lists, sta1, df, s=30,
                      legend=False,  plot_sta_names=False, labels=None,
                      xlim=None, ylim=None,figsize=(15,15),ax=None):
    '''
    Separated from spatial_stacking.py
    Plot a list of sublist that are station groups on the map.
    TODO
    
    '''
    
    colors = plt.cm.tab10(np.linspace(0,1,10))
    
    # Check if plot_sta_lists is a nested list or not
    if not isinstance(plot_sta_lists[0], np.ndarray) or not isinstance(plot_sta_lists[0], np.ndarray):
        plot_sta_lists=[plot_sta_lists]
        
    if not ax:
        fig,ax=plt.subplots(figsize=figsize)
    ax=plt.gca()
    ax.scatter(df.Lon, df.Lat, alpha=0.5, s=s, color=plt.cm.Greys(0.3))
    for i,sub_list in enumerate(plot_sta_lists):
        if labels ==None:
            label=None
        else:
            label=labels[i]
        df_selected = df[df['Station'].isin(sub_list)]
        ax.scatter(df_selected.Lon,df_selected.Lat, alpha=1, s=s, 
                   color=colors[i%len(colors)],label=label
                   )#,edgecolor='k')
    if plot_sta_names==True:
        #  A station location list sorted by the station numbers
        stn_coor_list = sorted(zip(df.Lon, df.Lat, df.Station),key=lambda x: x[2])
        for x, y, label in stn_coor_list:
            ax.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points",fontsize=3)
    stla1,stlo1=df[df['Station']==sta1].Lat.values[0],df[df['Station']==sta1].Lon.values[0]
    plt.plot(stlo1,stla1,marker='*',markersize=35,color='tab:green',label=r'$sta_1$',alpha=0.9,
             markeredgecolor='k',zorder=3,linestyle='None')
    plt.xlim(xlim)
    plt.ylim(ylim)
    ax. set_aspect('equal')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    
    if legend ==True:
        plt.legend(fontsize=20)
    
    return ax
