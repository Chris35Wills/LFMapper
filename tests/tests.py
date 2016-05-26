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

package_fail=0

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
"""
def test_01_standard_imports():
	try:
		import numpy
		import matplotlib.pyplot
	except:
		package_fail=1
		sys.exit("Check you have access to numpy and matplotlib")
	
def test_02_scipy_access():
	try:
		import scipy
	except:
		package_fail=1
		sys.exit("Access to scipy failed - check you have it installed - if using anaconda install using: conda install scipy")

def test_03_osgeo_access():
	try:
		import osgeo	
	except:
		package_fail=1
		sys.exit("osgeo not available - check you have it installed - if using anaconda install using: conda install -c osgeo gdal=1.11.4")

def test_04_bespoke_imports():
	### these are bespoke to this program
		
	try:
		from crevassemap import util 
		from crevassemap import raster_functions 
		from crevassemap import flatten
		from crevassemap import FT_spacing_orientation_stats
		from crevassemap import more_fft_functions
		from crevassemap import quiver_plotter
	except:
		package_fail=1
		sys.exit("Bespoke imports FAILED - check you are in the right directory to import the crevassemap module")

def test_05_access_smooth():
	try:
		from crevassemap.smoothfft import smooth
	except:
		package_fail=1
		sys.exit("smooth function can't be accessed - check access to crevassemap module")	

def test_06_numpy_nanmean():
	import numpy as np
	a=[1,2,3,4]
	
	try:
		np.nanmean(a)
	except:
		package_fail=1
		sys.exit("Numpy doesn't have acces to nanmean - Update Numpy to at least version 1.8.0")

##### Raster functions test
def test_98_load_envi_dimensions():
	
	if(package_fail==1):
		sys.exit("Can't test functions until package issues are resolved")
	
	elif(package_fail==1):
		image_array, post, (geotransform, inDs) = raster_functions.load_envi(envi_file_name)
	
		try:
			assert image_array.shape[0] == expect_cols
		except AssertionError:
			sys.exit("ENVI file loading not working properly - array object different size to specified image dimensions\n -- check file and path is valid")
		

def test_99_load_envi_post():
	
	if(package_fail==1):
		sys.exit("Can't test functions until package issues are resolved")
	
	elif(package_fail==1):
		image_array, post, (geotransform, inDs) = raster_functions.load_envi(non_envi_file_name)
	
		try:
			assert post == non_envi_post
		except AssertionError:
			sys.exit("ENVI file loading not working properly - observed post different to expected post\n -- check file and path is valid")
"""
##### Main Tests

from crevassemap import raster_functions, spacing, image_step_clean

"""
def test_100_full_run_ENVI():

	if(package_fail==1):
		sys.exit("Can't test program until package issues are resolved")

	elif(package_fail==0):
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
"""

def test_101_full_run_NON_ENVI():
		
	if(package_fail==1):
		sys.exit("Can't test program until package issues are resolved")

	elif(package_fail==0):
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
			sys.exit("Main code has broken down using a NON-ENVI file... consider changes since last commit")


