from __future__ import division

import os
import time as time # for reading in a timer
import numpy as np # maths functions (arrays etc.)
from numpy import *
import math
import copy as cp
from fractions import gcd


def snr(array, value):
	'''
	Calculates signal-to-noise value 
	based on standard deviations
	'''
	mean = np.nanmean(array)
	std = np.nanstd(array)
	return (value - mean) / std

##############################
## OLD SnR code (pre 14/11/14)
##############################

def solve(ratio):
	'''
	Simplifies a ratio based on common factors
	Input "ratio" is of format: '%i:%i'
	'''	
	numbers = [int(i) for i in ratio.split(':')]
	denominator = reduce(gcd,numbers)
	solved = [i/denominator for i in numbers]
	return ':'.join(str(i) for i in solved)


def SignalToNoise(array, array_max):
	'''
	Returns True or False depending on whether SnR exceeds a threshold number 
	of standard deviations. Calculates SnR based on the maximum peak vs. the 
	mean of the rest of the surface (omitting the maximum peak value)

	This could be further developed to take into account a kernel around the 
	peak, ultimately lowering the SnR (a wider peak shape having a smaller SnR 
	than a narrower peak)		
	'''
	array_max = array_max
	array_omit_max = array.copy()
	array_omit_max[array_omit_max == array_omit_max.max()] = float('nan')
	mean_array_omit_max = nanmean(array_omit_max)
	ratio = '%i:%i' %(int(array_max),int(mean_array_omit_max))
	ratio_2_solve = solve(ratio)
	SnR_float = array_max/mean_array_omit_max
	SD = np.nanstd(array_omit_max) # standard deviation
		
	if(SnR_float>(2*SD)):
		#print "SnR ratio acceptable - peak identified"
		return True
	else:
		#print "SnR ratio unacceptable - peak identified"
		return False

def SignalToNoise_with_output(array, array_max, imgout, ii, jj, stepsize):
	'''	
	Calculates SnR based on the maximum peak vs. the 
	mean of the rest of the surface (omitting the maximum peak value). 
	Returns a populaed SnR array.
	'''
	array_max = array_max
	array_omit_max = array.copy()
	array_omit_max[array_omit_max == array_omit_max.max()] = float('nan')
	mean_array_omit_max = nanmean(array_omit_max)
	SnR_float = array_max/mean_array_omit_max
	SD = np.nanstd(array_omit_max) # standard deviation

	##Populate SnR surface	
	nvars = 1
	vtuple = (array_max - mean_array_omit_max)/SD
	
	imgout[0][ii // stepsize, jj // stepsize] = vtuple
	return imgout


	
