"""
Various tests to ensure package visibility, function operation etc.

Whilst the program remains private, run these with nosetests.

Once program goes public, integrate with travis.
"""
import sys

# Some test data (and associated dimensions)
non_envi_file_name = 'tests/TEST_DATA/zebra.jpg'
non_envi_cols = 518
non_envi_rows = 386
non_envi_post = 1

envi_file_name = 'tests/TEST_DATA/helheim_hyperspec_subset.bin'
output_dir = 'tests/test_output'
expect_cols = 1000.
expect_rows = 1000.
#expect_post = 

def check_odd_step(val):
		try:
			assert val %2 !=0
		except AssertionError:
			sys.exit("Stepsize must be odd")


def check_odd_kernel(val):
	try:
		assert val %2 !=0
	except AssertionError:
		sys.exit("Kernel dimension must be odd")	

##### Test function imports
def test_standard_imports():
	try:
		import numpy
		import matplotlib.pyplot
	except:
		print("Standard imports FAILED - you need to install some packages.")
		print("\nCheck which of these you don't have:\n")
		print("    import numpy")
		print("    import matplotlib.pyplot")
	
def test_nonstandard_imports():
	try:
		### these are not often in python distributions
		from scipy import ndimage
		import scipy.signal
		import scipy.misc
		from osgeo import gdal, gdalconst # for reading in raster
	except:
		print("Non standard imports FAILED - you need to install some packages.")
		print("\nCheck which of these you don't have:\n")
		print("    from scipy import ndimage")
		print("    import scipy.signal")
		print("    import scipy.misc")
		print("    from osgeo import gdal, gdalconst # for reading in raster")
		

def test_bespoke_imports():
	### these are bespoke to this program
		
	try:
		import util 
		import raster_functions 
		import flatten
		import FT_spacing_orientation_stats
		import more_fft_functions
		import quiver_plotter
		from smoothfft import smooth
	except:
		print("Bespoke imports FAILED - you need to install some packages.")
		print("\nFunctions should be stored in these directories:\n")
		print("../")
		print("./smoothfft")
		print("\nThese functions should be present:\n")
		print("    import util")
		print("    import raster_functions")
		print("    import flatten")
		print("    import FT_spacing_orientation_stats")
		print("    import more_fft_functions")
		print("    import quiver_plotter")
		print("    from smoothfft import smooth")

##### Main Tests

from crevassemap import raster_functions, spacing, image_step_clean

def test_full_run_ENVI():

	try:
		step_range = ([101])#([3])
		kernel_range = ([9])#([3])

		check_odd_kernel(kernel_range[0])
		check_odd_step(step_range[0])

		date = "TEST_Helheim"
		spectrum_n = 1.5 ## noise value (2 = brown)

		image_array, post, envidata = raster_functions.load_envi(envi_file_name)

		for stepsize in step_range:
			for kernel_size in kernel_range:
				img = image_step_clean.image_step_clean(stepsize, image_array)
				spacing.find_spacings(img, date, kernel_size, stepsize, envidata, post, output_dir, spectrum_n)

	except:
		sys.exit("Main code has broken down using an ENVI file... consider changes since last commit")


def test_full_run_NON_ENVI():
		
	try:
		step_range = ([51])
		kernel_range = ([9])

		check_odd_kernel(kernel_range[0])
		check_odd_step(step_range[0])

		date = "TEST_zebra"
		spectrum_n = 1.5 ## noise value (2 = brown)

		image_array, post, envidata = raster_functions.load_envi(non_envi_file_name)

		for stepsize in step_range:
			for kernel_size in kernel_range:
				img = image_step_clean.image_step_clean(stepsize, image_array)
				spacing.find_spacings(img, date, kernel_size, stepsize, envidata, post, output_dir, spectrum_n)

	except:
		print("Main code has broken down using a NON-ENVI file... consider changes since last commit")


##### Raster functions test
def test_load_envi_dimensions():
	
	image_array, post, (geotransform, inDs) = raster_functions.load_envi(envi_file_name)
	
	try:
		assert image_array.shape[0] == expect_cols
	except AssertionError:
		print("ENVI file loading not working properly - array object different size to specified image dimensions\n -- check file and path is valid")


def test_load_envi_post():
	
	image_array, post, (geotransform, inDs) = raster_functions.load_envi(non_envi_file_name)
	
	try:
		assert post == non_envi_post
	except AssertionError:
		print("ENVI file loading not working properly - observed post different to expected post\n -- check file and path is valid")


"""
raster_functions (COMPLETE) #~\GitHub\Python_scripts\newstart\crevassemap
util.check_output_dir() #~\GitHub\Python_scripts\newstart\crevassemap

image_step_clean (COMPLETE - NO IMPORTS) #~\GitHub\Python_scripts\newstart\crevassemap

spacing (YES) #~\GitHub\Python_scripts\newstart\crevassemap

smooth.smooth_fft                           #~\GitHub\Python_scripts\newstart\crevassemap\smoothfft
flatten.flatten_spectrum 					#~\GitHub\Python_scripts\newstart\crevassemap
SnR_function.snr                            #~\GitHub\Python_scripts\functions >> ~\GitHub\Python_scripts\newstart\crevassemap\imported_from_functions
more_fft_functions.border_indent            #~\GitHub\Python_scripts\newstart\crevassemap
util.check_output_dir						#~\GitHub\Python_scripts\newstart\crevassemap
plots.plot_image 							#~\GitHub\Python_scripts\functions >> ~\GitHub\Python_scripts\newstart\crevassemap\imported_from_functions

util.check_output_dir 							   #~\GitHub\Python_scripts\newstart\crevassemap
raster_functions.ENVI_raster_binary_from_2d_array  #~\GitHub\Python_scripts\newstart\crevassemap

util.trim_constant_rows_cols                #~\GitHub\Python_scripts\newstart\crevassemap
FT_spacing_orientation_stats.write_stats    #~\GitHub\Python_scripts\newstart\crevassemap

quiver_plotter.quiver_plot                  #~\GitHub\Python_scripts\newstart\crevassemap     << imports cleaned up

util.trim_constant_rows_cols            #~\GitHub\Python_scripts\newstart\crevassemap
raster_functions.load_envi              #~\GitHub\Python_scripts\newstart\crevassemap 
"""
