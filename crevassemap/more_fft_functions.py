from __future__ import division
"""
import os
import time as time # for reading in a timer
import numpy as np # maths functions (arrays etc.)
import math
from matplotlib import pyplot as plt # for ploting
from scipy import signal # for convolution function
import scipy.signal
from scipy import ndimage # for resampling image
from scipy.fftpack import fft2
from matplotlib import cm # colour mapping
import matplotlib as matplotlib
import matplotlib.pyplot as plt
import copy as cp
from numpy import *
import datetime
import random
from scipy import ndimage
from scipy import misc
from scipy.stats import rankdata
from time import gmtime, strftime
import pylab as pl
from glob import glob
from osgeo import gdal, gdalconst # for reading in raster
from osgeo.gdalconst import * # for reading in raster
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

import sys
sys.path.append("./smoothfft")
sys.path.append("./imported_from_functions")

import FFT_functions            #~\GitHub\Python_scripts\functions >> ~\GitHub\Python_scripts\newstart\crevassemap\imported_from_functions
import FFT_filter_functions     #~\GitHub\Python_scripts\functions >> ~\GitHub\Python_scripts\newstart\crevassemap\imported_from_functions
import raster_functions         #~\GitHub\Python_scripts\newstart\crevassemap
import Filter_functions 		#~\GitHub\Python_scripts\functions >> ~\GitHub\Python_scripts\newstart\crevassemap\imported_from_functions
import FFT_quadrant_processing  #~\GitHub\Python_scripts\functions >> ~\GitHub\Python_scripts\newstart\crevassemap\imported_from_functions
import FFT_functions_clean      #~\GitHub\Python_scripts\functions >> ~\GitHub\Python_scripts\newstart\crevassemap\imported_from_functions
import raster_functions 		#~\GitHub\Python_scripts\newstart\crevassemap
import smooth                   #~\GitHub\Python_scripts\newstart\crevassemap\smoothfft
reload(FFT_functions)
reload(FFT_filter_functions)
reload(raster_functions)
reload(Filter_functions)
reload(FFT_quadrant_processing)
reload(FFT_functions_clean)
reload(raster_functions)
reload(smooth)
"""

def border_indent(kernel_size, nxwind, nywind):
	'''
	Calculates how far into an image a pixel can be sampled to ensure a full 
	kernel can be sampled. Without "stepping in" from the perimeter of a 
	given image, part of the kernel - centred around the pixel position - would 
	fall outside of the main image/array
	'''
	window_border_indent = int((kernel_size - 1)/2 )
	window_border_indent_end_X = int(nxwind - window_border_indent)
	window_border_indent_end_Y = int(nywind - window_border_indent) 
	
	return window_border_indent, window_border_indent_end_X, window_border_indent_end_Y


def window_instance_dimensions(ii, jj, window_border_indent, nxwind, nywind, kernel_size, modification_value=1):
	'''
	Calculate the max and min array coordinate positions (rows/cols) for a kernel at a given pixel position
	where window_border_indent == 0.5 * kernel size
	'''
	imin=max(0,ii-(window_border_indent*modification_value)) # gets the maximum of either 0 or i-kernel_size/2...
	imax=min(nywind-1,ii+(window_border_indent*modification_value))+1
	jmin=max(0,jj-(window_border_indent*modification_value))
	jmax=min(nxwind-1,jj+(window_border_indent*modification_value))+1
	
	calc_moving_window_size_x = imax - imin 
	calc_moving_window_size_y = jmax- jmin

	return imin, imax, jmin, jmax, calc_moving_window_size_x, calc_moving_window_size_y

if __name__ == "__main__":
	print("Run from import.")