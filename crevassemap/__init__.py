from distutils.version import StrictVersion
import numpy as np
import sys

if not (np.version.version>=StrictVersion('1.8.0')):
	sys.exit("Update numpy to at least version 1.8.0")
