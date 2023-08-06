# -*- coding: utf-8 -*-
"""
Created on Wed May 11 10:42:34 2016

@author: deborahkhider

Initializes the Pyleoclim module

"""
#Import all the needed packages


import lipd as lpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
import sys
import os
from matplotlib import gridspec

#Import internal packages to pyleoclim
from .pkg_resources.Map import *
from .pkg_resources.TSPlot import *
from .pkg_resources.LiPDutils import *
from .pkg_resources.Basic import *
from .pkg_resources.SummaryPlots import *

# Load the LiPDs present in the directory
#lpd.loadLipds()

# Get the timeseries objects

#time_series = lpd.extractTs()

# Set the default palette for plots

plot_default = {'ice/rock': ['#FFD600','h'],
                'coral': ['#FF8B00','o'],
                'documents':['k','p'],
                'glacier ice':['#86CDFA', 'd'],
                'hybrid': ['#00BEFF','*'],
                'lake sediment': ['#4169E0','s'],
                'marine sediment': ['#8A4513', 's'],
                'sclerosponge' : ['r','o'],
                'speleothem' : ['FF1492','d'], 
                'wood' : ['#32CC32','^'],
                'molluskshells' : ['#FFD600','h'],
                'peat' : ['#2F4F4F','*']} 

# Mapping
def MapAll(markersize = int(50), saveFig = True, dir="", format='eps'):
    """
    Map all the available records loaded into the LiPD working directory by archiveType.
    Arguments:
      - path: the path where the liPD files are saved. If not given, will trigger the LiPD GUI
      - markersize: default is 50
      - saveFig: default is to save the figure
      - dir: the full path of the directory in which to save the figure. If not provided, creates
      a default folder called 'figures' in the LiPD working directory (lipd.path). 
      - format: One of the file extensions supported by the active backend. Default is "eps".
      Most backend support png, pdf, ps, eps, and svg. 
    """
    # Make sure there are LiPD files to plot
    if not hasattr(lpd,'path'):
        lpd.loadPath()
        lpd.loadLipds()
        
    map1 = Map(plot_default)
    map1.map_all(markersize=markersize, saveFig = saveFig, dir=dir, format=format)

def MapLiPD(name="",gridlines = False, borders = True, \
        topo = True, markersize = int(100), marker = "default", \
        saveFig = True, dir = "", format="eps"):
    """
    Makes a map for a single record. 
    Arguments:
     - name: the name of the LiPD file. **WITH THE .LPD EXTENSION!**.
     If not provided, will prompt the user for one.
     - gridlines: Gridlines as provided by cartopy. Default is none (False).
     - borders: Pre-defined country boundaries fron Natural Earth datasets (http://www.naturalearthdata.com).
     Default is on (True). 
     - topo: Add the downsampled version of the Natural Earth shaded relief raster. Default is on (True)
     - markersize: default is 100
     - marker: a string (or list) containing the color and shape of the marker. Default is by archiveType.
     Type pyleo.plot_default to see the default palette. 
     - saveFig: default is to save the figure
     - dir: the full path of the directory in which to save the figure. If not provided, creates
      a default folder called 'figures' in the LiPD working directory (lipd.path).  
     - format: One of the file extensions supported by the active backend. Default is "eps".
      Most backend support png, pdf, ps, eps, and svg.
    """
    # Make sure there are LiPD files to plot
    if not hasattr(lpd,'path'):
        lpd.loadPath()
        lpd.loadLipds()
        
    map1 = Map(plot_default)
    map1.map_one(name=name,gridlines = gridlines, borders = borders, \
        topo = topo, markersize = markersize, marker = marker, \
        saveFig = saveFig, dir = dir, format=format)

# Plotting

def plotTS(timeseries_dict = "", timeseries = "", x_axis = "", markersize = 50,\
            marker = "default", saveFig = True, dir = "",\
            format="eps"):
    """
    Plot a single time series. 
    Arguments:
    - timeseries_dict: A dictionary of timeseries. Is obtained by using lipd.extractTS().
    If neither a dictionary of timeseries is given, the software will fecth the dictionary automatically.
    - A timeseries: By default, will prompt the user for one. 
    - x_axis: The representation against which to plot the paleo-data. Options are "age",
    "year", and "depth". Default is to let the system choose if only one available or prompt
    the user. 
    - markersize: default is 50. 
    - marker: a string (or list) containing the color and shape of the marker. Default is by archiveType.
     Type pyleo.plot_default to see the default palette.
    - saveFig: default is to save the figure
    - dir: the full path of the directory in which to save the figure. If not provided, creates
      a default folder called 'figures' in the LiPD working directory (lipd.path). 
    - format: One of the file extensions supported by the active backend. Default is "eps".
      Most backend support png, pdf, ps, eps, and svg.
    """
    if not timeseries_dict and not timeseries:
        timeseries_dict = getTSDict()
    plot1 = Plot(plot_default, timeseries_dict)
    plot1.plotoneTSO(new_timeseries = timeseries, x_axis = x_axis, markersize = markersize,\
                   marker = marker, saveFig = saveFig, dir = dir,\
                   format=format)

# Statistics

def TSstats(timeseries_dict = "", timeseries=""):
    """
    Return the mean and standard deviation of the paleoData values of a timeseries
    Arguments:
    - Timeseries: sytem will prompt for one if not given
    """
    if not timeseries_dict and not timeseries:
        timeseries_dict = getTSDict()
    basic1 = Basic(timeseries_dict)
    mean, std = basic1.simpleStats(timeseries = timeseries)
    return mean, std

def TSbin(timeseries_dict = "", timeseries="", x_axis = "", bin_size = "", start = "", end = ""):
    """
    Bin the paleoData values of the timeseries
    Arguments:
      - timeseries_dict: A dictionary of timeseries. Is obtained by using lipd.extractTS().
    If neither a dictionary of timeseries is given, the software will fecth the dictionary automatically.
      - Timeseries. By default, will prompt the user for one.
      - x-axis: The representation against which to plot the paleo-data. Options are "age",
    "year", and "depth". Default is to let the system choose if only one available or prompt
    the user. 
      - bin_size: the size of the bins to be used. By default, will prompt for one
      - start: Start time/age/depth. Default is the minimum 
      - end: End time/age/depth. Default is the maximum
    Outputs:
      - binned_data: the binned output
      - bins: the bins (centered on the median, i.e. the 100-200 bin is 150)
      - n: number of data points in each bin
      - error: the standard error on the mean in each bin
    """
    if not timeseries_dict and not timeseries:
        timeseries_dict = getTSDict()
        timeseries = getTSO(timeseries_dict)
    elif not timeseries:
        timeseries = getTSO(timeseries_dict)
    bins, binned_data, n, error = Basic.bin_data(timeseries = timeseries,\
                x_axis = x_axis, bin_size = bin_size, start = start, end = end)
    return bins, binned_data, n, error

def TSinterp(timeseries_dict = "", timeseries="", x_axis = "", interp_step = "", start = "", end = ""):
    """
    Simple linear interpolation
    Arguments:
      - timeseries_dict: A dictionary of timeseries. Is obtained by using lipd.extractTS().
    If neither a dictionary of timeseries is given, the software will fecth the dictionary automatically.
      - Timeseries. Default is blank, will prompt for it
      - x-axis: The representation against which to plot the paleo-data. Options are "age",
    "year", and "depth". Default is to let the system choose if only one available or prompt
    the user. 
      - interp_step: the step size. By default, will prompt the user. 
      - start: Start time/age/depth. Default is the minimum 
      - end: End time/age/depth. Default is the maximum
    Outputs:
      - interp_age: the interpolated age/year/depth according to the end/start and time step
      - interp_values: the interpolated values
    """
    if not timeseries_dict and not timeseries:
        timeseries_dict = getTSDict()
        timeseries = getTSO(timeseries_dict)
    elif not timeseries:
        timeseries = getTSO(timeseries_dict)
    interp_age, interp_values = Basic.interp_data(timeseries = timeseries,\
                x_axis = x_axis, interp_step = interp_step, start= start, end=end)
    return interp_age, interp_values
    
# SummaryPlots
def BasicSummary(timeseries_dict = "", timeseries = "", x_axis="", saveFig = True,
                     format = "eps", dir = ""):
    """
    Makes a basic summary plot
    1. The time series
    2. Location map
    3. Age-Depth profile if both are available from the paleodata
    4. Metadata

    **Note**: The plots use default setting from the MapLiPD and plotTS method.
    
    Arguments:
      - timeseries_dict: A dictionary of timeseries. Is obtained by using lipd.extractTS().
    If neither a dictionary of timeseries is given, the software will fecth the dictionary automatically.
      - timeseries: By default, will prompt for one.
      - x-axis: The representation against which to plot the paleo-data. Options are "age",
    "year", and "depth". Default is to let the system choose if only one available or prompt
    the user.
      - saveFig: default is to save the figure
      - dir: the full path of the directory in which to save the figure. If not provided, creates
      a default folder called 'figures' in the LiPD working directory (lipd.path). 
      - format: One of the file extensions supported by the active backend. Default is "eps".
      Most backend support png, pdf, ps, eps, and svg.
    """
    if not timeseries_dict and not timeseries:
        timeseries_dict = getTSDict()
    plt1 = SummaryPlots(timeseries_dict, plot_default)
    plt1.basic(x_axis=x_axis, new_timeseries = timeseries, saveFig=saveFig,\
               format = format, dir = dir)

