from __future__ import division

import time
import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage

# local
import flatten
import FT_spacing_orientation_stats
import more_fft_functions
import quiver_plotter
import util
from smoothfft import smooth
import plots, SnR_function
reload(plots)
reload(quiver_plotter)

def find_spacing_of_image(image, spectrum_n=1.0):
	xsize, ysize = image.shape
	assert xsize == ysize
	assert xsize % 2 == 1
	return find_spacing_at_point(image, xsize//2, ysize//2, xsize, spectrum_n)

def find_spacing_at_point(image, x, y, kernel_size, spectrum_n=1.0, show_fft=0):
	'''
	For a given image array, a subimage is created spanning half of the kenel size around position (x,y).
	The subimage is then gaussian smoothed and converted to frequency space with the gibbs cross effect 
	being removed. This image is then flattened using a user specifed degree of noise. Th maximum of the 
	FT - specifically it's position relative to the FT origin and its related orientation (degN). 
	Signal-to-noise is then calculated - this can be used to ascertain the validity of a given maximum peak.

	Requires access to:
	SnR_function.snr()
	smooth.smooth_fft()
	'''
	half_kernel = (kernel_size-1)//2
	subimg = image[(x - half_kernel):(x + half_kernel + 1), (y - half_kernel):(y + half_kernel + 1)]
	assert subimg.shape == (kernel_size, kernel_size), "Shape is %s, kernel is %d" % (subimg.shape, kernel_size)

	blurred = ndimage.filters.gaussian_filter(subimg, sigma=1.0, order=0, mode='reflect')

	fftimg = smooth.smooth_fft(blurred)

	flattened = flatten.flatten_spectrum(fftimg, n=spectrum_n)

	if show_fft==1: 
		plt.imshow(flattened)
		plt.colorbar()
		plt.show()

	half_fft = np.log(flattened)[:,:(half_kernel + 1)]

	fft_max = half_fft.max()

	if np.isnan(fft_max):
		raise Exception # TODO

	max_1d = np.argmax(half_fft)
	max_i, max_j = np.unravel_index(max_1d, half_fft.shape)

	center_i = half_kernel
	center_j = half_kernel

	half_fft[center_i, center_j] = np.nan

	angle = -np.degrees(np.arctan2(max_j - center_j, max_i - center_i))

	while angle < 0:
		angle += 180

	while angle > 180:
		angle -= 180    

	dist_frq = ((max_i - center_i) ** 2 + (max_j - center_j) ** 2) ** 0.5
	dist_px = kernel_size / dist_frq

	snr = SnR_function.snr(half_fft, fft_max)

	return angle, dist_px, snr

def find_spacings(image_array, date, kernel_size, stepsize, envidata, post, output_dir, spectrum_n=1.0, interact=False):
	'''
	Main workhorse of the whole FT program - for a provided input image a moving window - of a prior specified 
	size - is iterated across an FT array of the original image. This returns new arrays representing maximum 
	peak spacing, orientation and related signal-to-noise ratio (standard deviation of a given point over the 
	mean). These arrays are then plotted and converted to binary files with headers matching that of the 
	original input file - the pixels are rescaled to account for the step frequency of the moving window.

	Requires access to:
	find_spacing_at_point()
	more_fft_functions.border_indent()
	plots.plot_image()
	util.trim_constant_rows_cols
	'''	
	startTime = time.time()

	nywind,nxwind = image_array.shape

	opath = output_dir + '/%s_win_%s_step_%s' % (date, kernel_size, stepsize)

	###########################
	## SET MOVING WINDOW UP  ##
	###########################

	if kernel_size % 2 == 0 or kernel_size < 3:
		error_msg = "kernel is even - it needs to be odd and at least of a value of 3"
		sys.exit(error_msg)

	space = np.zeros((nywind // stepsize, nxwind // stepsize))
	orientation = np.zeros((nywind // stepsize, nxwind // stepsize))
	SnR_imgout = np.zeros((nywind // stepsize, nxwind // stepsize))
	orig = np.zeros((nywind // stepsize, nxwind // stepsize))

	window_border_indent, window_border_indent_end_X, window_border_indent_end_Y = more_fft_functions.border_indent(kernel_size, nxwind, nywind)


	time_stamp = time.strftime("%H.%M.%S")
	file_name = "%s/FT_POST_log_%s_%s.txt" %(opath, date, time_stamp)
	util.check_output_dir(file_name)
	with open( file_name, 'w') as f:
		f.write("Post: %f\n" %post)
		f.write("Image dimensions (x,y): %f, %f\n" %(nywind,nxwind))
		f.write("Noise value: %f\n" %(spectrum_n))
		f.write("Kernel size: %f\n" %(kernel_size))
		f.write("Stepsize: %f\n" %(stepsize))
		f.write("%s, %s, %s\n" %("Feature orientation", "distance (frq)", "distance (m)"))

	for out_i, ii in enumerate(range(window_border_indent, window_border_indent_end_Y, stepsize)):
		for out_j, jj in enumerate(range(window_border_indent, window_border_indent_end_X, stepsize)):
			angle, dist, snr = find_spacing_at_point(image_array, ii, jj, kernel_size, spectrum_n, show_fft=0)
			space[out_i, out_j] = dist * post
			orientation[out_i, out_j] = angle
			SnR_imgout[out_i, out_j] = snr
			orig[out_i, out_j] = image_array[ii, jj]

	print "PRINTING IMAGES...."
	img_prefix = opath + '/%s_winsize_%i_stepsize_%i_nvalue_%f_%s' % (date, kernel_size, stepsize, spectrum_n, time_stamp)
	new_post = post * stepsize

 	# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
	# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< PROBLEM inside plot function if envidata==False such as using sine_wave_TEST.py (see plots.py)	
	plots.plot_image(space, 'Crevasse spacing (m)', img_prefix + '_spacing_m', envidata, new_post, remove_empty_cols=1)
	plots.plot_image(orientation, 'Crevasse orientation (degN.)', img_prefix + '_orientation', envidata, new_post, remove_empty_cols=1)
	plots.plot_image(SnR_imgout, 'Signal-to-noise (%s)' % date, img_prefix + '_snr', envidata, new_post, remove_empty_cols=1)
	plots.plot_image(orig, 'Original input image (%s)' % date, img_prefix + '_original', envidata, new_post, remove_empty_cols=1)

	spacing_no_zeros = util.trim_constant_rows_cols(space)
	orientation_no_zeros = util.trim_constant_rows_cols(orientation)


	FT_spacing_orientation_stats.write_stats(output_dir + '/spacing_stats.txt', spacing_no_zeros, date, kernel_size, stepsize)
	FT_spacing_orientation_stats.write_stats(output_dir + '/orientation_stats.txt', orientation_no_zeros, date, kernel_size, stepsize)

	## CREATE QUIVER PLOT

	plot_title = "%s_winsize_%i_stepsize_%i" %(date, kernel_size, stepsize)

	quiver_plotter.quiver_plot(orientation, space, opath, plot_title, img_prefix + '_quiver', interact=interact)

	endTime = time.time()
	totalTime = endTime - startTime
	print "Run took %f seconds to run" %(totalTime)

if __name__ == "__main__":
	print("Run from import.")