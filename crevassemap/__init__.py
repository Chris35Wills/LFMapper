from distutils.version import StrictVersion
import numpy as np
import matplotlib
import sys
import os

if not (np.version.version>=StrictVersion('1.8.0')):
	sys.exit("Update numpy to at least version 1.8.0")

# to ensure plotting works if display isn't set: http://stackoverflow.com/questions/2801882/generating-a-png-with-matplotlib-when-display-is-undefined
havedisplay = "DISPLAY" in os.environ
try:
	assert havedisplay == True
except AssertionError:
	print("DISPLAY variable not set (no X11 forwarding) - changing matplotlib backend to Agg")
	matplotlib.use('Agg')