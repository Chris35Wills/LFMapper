"""
KERNEL SIZE ESTIMTION

Functions to assess optimum kernel size when using LFMapper

Approximating image feature spacings using an FT approach as well as the variable size of the kernel about 
a specified pixel - once run, spacings as per window size can be considered and the most appropriate 
feature spacing chosen to approximate minimum window size when running the full 2D step FT method.

Unlike approx_feature_spacing.py this method does not have the issues associated with non square images and 
edge effects (as a whole image, including areas not of interest, is not directly being considered). Too 
large a window size should be avoided to keep the area being tested within the area of interest (too big a 
window could strectch out of the AOI)

CSV files containing kernel size and maximum associated point spacing are saved.

Modified: January 2018

__author__ Chris Williams and Martin O'Leary
__date__ 16th April 2018
__email__ chris.neil.wills@gmail.com
"""

import sys
import csv 
from matplotlib import pyplot as plt 
#sys.path.append('N:/Github/LFMapper')
from crevassemap import raster_functions, spacing, util


# https://codereview.stackexchange.com/questions/115954/writing-lists-to-csv-file
def write_list_to_file(guest_list, filename):
    """Write the list to csv file."""

    with open(filename, "w") as outfile:
        for entries in guest_list:
            outfile.write(str(entries))
            outfile.write("\n")

#def window_estimator(path, opath, input_image, label):
def window_estimator(path, opath, input_image, plotting=False, plotting_binary=0):

	#	path = 'C:/Users/chrwil/Desktop/Hofsjokull_data/hofsjokull-2008-cmb-v1'
	#	opath= 'C:/Users/chrwil/Desktop/Hofsjokull_data/outputs_5m'
	#	input_image = "%s/hofsjokull_FLAT_5m_SUBSET.tif" %(path)
	#	aoi = 'hofs_5m_sub'

	#path = "N:/Github/BGS/bgs_projects/bgs__crevasse_risk_mapping/mars/"
	#opath = 'C:/Users/chrwil/Desktop/mars/mars_dune_ORIENTATION_SPACING/'
	#input_image = "%s/mars_dune_image.png" %(path)

	util.check_output_dir(opath)

	spectrum_n=3.0 # flattening power value (see ./understanding_the_program/test_effect_of_flattening_on_peak_identification.py for more help)

	#for i in range(len(input_image)):

	image_array, post, image_data = raster_functions.load_dem(input_image, gdal_driver='PNG')


	pixelWidth=image_data[0][1]

	if plotting:
		plt.imshow(image_array, interpolation='none')
		plt.title('Original image')
		plt.show()

	# Get image pixel dimensions
	cols,rows=image_array.shape

	if(cols != rows):
		print("Approximating centre row and column...")	

	centre_col = cols//2 # gets an integer (the //)
	centre_row = rows//2 # gets an integer (the //)

	#image_array[centre_row, centre_col] ## This doesn't really do anything...

	nyqvist_frq = (rows-1)//2

	kernel = 3
	kernel_size_LIST = []
	feature_spacing_m_LIST = []
	snr_LIST = []

	while kernel < centre_row//2 and kernel < centre_col//2:

		try:
			_, max_dist_px, snr = spacing.find_spacing_at_point(image_array, 
															centre_row, 
															centre_col, 
															kernel, 
															spectrum_n=spectrum_n, 
															show_fft=plotting_binary)	## how is the noise (spectrum_n) value chosen?
		except AssertionError:
			print("Assertion Error relating to window size... still need to fix this")

		max_dist_m = max_dist_px*pixelWidth

		#print("===========================")
		#print("Kernel: ", kernel)
		#print("Spacing (pixels): ", max_dist_px)
		#print("Spacing (m): ", max_dist_m)

		kernel_size_LIST.append(kernel)
		feature_spacing_m_LIST.append(max_dist_m)
		snr_LIST.append(snr)


		# Increase kernel size (add 2 each time i.e. 3,5,7,9,11,13...)
		#kernel = 2 * int(kernel * 1.2 / 2) + 1 ## what does this bit do??
		kernel=kernel+2
		print("kernel size: %s" %kernel)
	
	################# DEAL WITH OUTPUTS...

	# Write feature_spacing_m_LIST and kernel_size_LIST to file
	write_list_to_file(feature_spacing_m_LIST, "%s/window_check__feature_spacings.csv" %opath)
	write_list_to_file(kernel_size_LIST, "%s/window_check__kernel_size.csv" %opath)

	# Create plot
	plt.clf()
	plt.plot(kernel_size_LIST, feature_spacing_m_LIST)
	plt.title("Feature spacing vs. kernel size")
	plt.xlabel("Kernel spacing (px)")
	plt.ylabel("Feature spacing (px)")
	plt.savefig("%s/kernel_spacing_px.png" %opath)
	#plt.show()