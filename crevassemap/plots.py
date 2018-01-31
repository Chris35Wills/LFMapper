from __future__ import division

import matplotlib.pyplot as plt
from matplotlib import cm
import scipy.misc

import crevassemap.util as util
import crevassemap.raster_functions as raster_functions


#def save_array_as_txt(arr, ofile):
#	"""
#	Saves a numpy array as a png file
#
#	NOT RECOMMENDED FOR LARGE FILES
#	"""	
#	numpy.savetxt(fname, X, fmt='%.18e', delimiter=' ', newline='\n', header='', footer='', comments='# ')[source]

def save_array_as_image(arr, ofile):
	"Saves a numpy array as an image file - type depends on extension set by user"	
	util.check_output_dir(ofile)
	scipy.misc.imsave(ofile, arr)

def plot_image(img, title, filename, envidata, post, remove_empty_cols=0):
	'''	
	Plots a given image as a png and also converts the input to a binary using 
	raster_functions.ENVI_raster_binary_from_2d_array() - this requires geotransform 
	info to be available (see raster_functions.load_envi()). ENVI output is hardwired.
	'''
	util.check_output_dir(filename)

	#print("Inside plot image...")
	#print(img.shape)	
	
	if remove_empty_cols == 1:
		img = util.trim_constant_rows_cols(img) 

	#fig, ax = plt.subplots()
	#cax = ax.imshow(img, cmap=cm.coolwarm, interpolation='none')
	#ax.set_xticklabels(" ")
	#ax.set_yticklabels(" ")
	#ax.set_title(title)
	#cbar=fig.colorbar(cax)
	plt.imshow(img, cmap=cm.coolwarm)
	plt.title(title)
	plt.colorbar()
	plt.savefig(filename + '.png', dpi=300, transparent=True)
	plt.clf()
	

	## put into new function.... <<<<<<<<<<<<<<<<<<<<<<<<<<<
	if envidata != False:
		print("Geospatial data provided :)")
		raster_functions.ENVI_raster_binary_from_2d_array(envidata, filename + '.bin', post, img)
	# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
	# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< PROBLEM WITH THIS CATCH STILL - ARRAYS DEVELOPING ZERO AXIS....
	else:
		print("No geospatial data provided - saving as txt file.")
		ofile="%s.png" %filename
		save_array_as_image(img, ofile)
	


