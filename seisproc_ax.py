#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions for plotting. 

The scripts are distributed under the terms of the GNU General Public License as 
published by the Free Software Foundation (version 3 or later version).

@author: Hilary Chang

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.text import Annotation
from matplotlib.transforms import Affine2D
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

def line(x,a,b=0):
    '''
    Get y given x.
    '''
    return a*x+b

def inverse_line(y,a,b=0):
    '''
    Get x given y.
    '''
    return (y-b)/a


class LineAnnotation(Annotation):
    """
    A sloped annotation to *line* at position *x* with *text*
    Optionally an arrow pointing from the text to the graph at *x* can be drawn.
    Usage
    -----
    fig, ax = subplots()
    x = linspace(0, 2*pi)
    line, = ax.plot(x, sin(x))
    ax.add_artist(LineAnnotation("text", line, 1.5))
    """

    def __init__(
        self, text, line, x, xytext=(0, 5), textcoords="offset points", **kwargs
    ):
        """Annotate the point at *x* of the graph *line* with text *text*.

        By default, the text is displayed with the same rotation as the slope of the
        graph at a relative position *xytext* above it (perpendicularly above).

        An arrow pointing from the text to the annotated point *xy* can
        be added by defining *arrowprops*.

        Parameters
        ----------
        text : str
            The text of the annotation.
        line : Line2D
            Matplotlib line object to annotate
        x : float
            The point *x* to annotate. y is calculated from the points on the line.
        xytext : (float, float), default: (0, 5)
            The position *(x, y)* relative to the point *x* on the *line* to place the
            text at. The coordinate system is determined by *textcoords*.
        **kwargs
            Additional keyword arguments are passed on to `Annotation`.

        See also
        --------
        `Annotation`
        `line_annotate`
        """
        assert textcoords.startswith(
            "offset "
        ), "*textcoords* must be 'offset points' or 'offset pixels'"

        self.line = line
        self.xytext = xytext

        # Determine points of line immediately to the left and right of x
        xs, ys = line.get_data()

        def neighbours(x, xs, ys, try_invert=True):
            inds, = np.where((xs <= x)[:-1] & (xs > x)[1:])
            if len(inds) == 0:
                assert try_invert, "line must cross x"
                return neighbours(x, xs[::-1], ys[::-1], try_invert=False)

            i = inds[0]
            return np.asarray([(xs[i], ys[i]), (xs[i+1], ys[i+1])])
        
        self.neighbours = n1, n2 = neighbours(x, xs, ys)
        
        # Calculate y by interpolating neighbouring points
        y = n1[1] + ((x - n1[0]) * (n2[1] - n1[1]) / (n2[0] - n1[0]))

        kwargs = {
            "horizontalalignment": "center",
            "rotation_mode": "anchor",
            **kwargs,
        }
        super().__init__(text, (x, y), xytext=xytext, textcoords=textcoords, **kwargs)

    def get_rotation(self):
        """Determines angle of the slope of the neighbours in display coordinate system
        """
        transData = self.line.get_transform()
        dx, dy = np.diff(transData.transform(self.neighbours), axis=0).squeeze()
        return np.rad2deg(np.arctan2(dy, dx))

    def update_positions(self, renderer):
        """Updates relative position of annotation text
        Note
        ----
        Called during annotation `draw` call
        """
        xytext = Affine2D().rotate_deg(self.get_rotation()).transform(self.xytext)
        self.set_position(xytext)
        super().update_positions(renderer)

def line_annotate(text, line, x, *args, **kwargs):
    """
    Add a sloped annotation to *line* at position *x* with *text*

    Optionally an arrow pointing from the text to the graph at *x* can be drawn.

    Usage
    -----
    x = linspace(0, 2*pi)
    line, = ax.plot(x, sin(x))
    line_annotate("sin(x)", line, 1.5)

    See also
    --------
    `LineAnnotation`
    `plt.annotate`
    """
    ax = line.axes
    a = LineAnnotation(text, line, x, *args, **kwargs)
    if "clip_on" in kwargs:
        a.set_clip_path(ax.patch)
    ax.add_artist(a)
    return a