from __future__ import division

import os
import numpy as np
import math
from numpy import *

import util

def write_stats(filename, data, date, kernel_size, stepsize):
	util.check_output_dir(filename)

	if os.path.exists(filename):
		f = open(filename, 'a')
	else:
		f = open(filename, 'w')
		f.write("Run, min, max, mean, median, std.dev., UQ, LQ, IQR\n")

	f.write("%s_win_%s_step_%s, %f, %f, %f, %f, %f, %f, %f, %f\n" %(date, kernel_size, stepsize, 
		np.amin(data), np.amax(data), np.mean(data), 
			np.median(data), np.std(data), np.percentile(data, 75), 
				np.percentile(data, 25), (np.percentile(data, 75) - np.percentile(data, 25))))
	f.close()

if __name__ == "__main__":
	print("Run from import.")