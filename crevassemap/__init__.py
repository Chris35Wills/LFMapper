from distutils.version import StrictVersion
import numpy as np
import matplotlib
import sys

if not (np.version.version>=StrictVersion('1.8.0')):
	sys.exit("Update numpy to at least version 1.8.0")

# to ensure plotting works if diaply isn't set: http://stackoverflow.com/questions/2801882/generating-a-png-with-matplotlib-when-display-is-undefined
matplotlib.use('Agg')