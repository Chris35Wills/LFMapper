"""
Various tests to ensure package visibility, function operation etc.

Whilst the program remains private, run these with nosetests.

Once program goes public, integrate with travis.
"""
import sys
from distutils.version import StrictVersion

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

##### Test python version

def test_python_version(): 
	
	try:
		v = sys.version_info[0] + sys.version_info[1]/10.
		assert v == 2.7
	except:
		sys.exit("FATAL ERROR: Requires python v2.7 to run - you have v%i.%i installed" %(sys.version_info[0], sys.version_info[1]))


##### Test function imports

def test_numpy_access():
	try:
		import numpy
	except:
		sys.exit("FATAL ERROR: Access to numpy failed")

def test_numpy_version():
	
	try:
		import numpy as np
		from distutils.version import StrictVersion
		assert np.version.version>=StrictVersion('3.8.0')
	except:
		sys.exit("FATAL ERROR: Update numpy to at least version 1.8.0")

def test_matplotlib_access():
	try:
		import matplotlib
	except:
		sys.exit("FATAL ERROR: Access to matplotlib failed")

def test_scipy_access():
	try:
		import scipy
	except:
		sys.exit("FATAL ERROR: Access to scipy failed - check you have it installed - if using anaconda install using: conda install scipy")

def test_osgeo_access():
	try:
		import osgeo	
	except:
		sys.exit("FATAL ERROR: osgeo not available - check you have it installed - if using anaconda install using: conda install -c osgeo gdal=1.11.4")

def test_bespoke_imports():
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
		sys.exit("FATAL ERROR: crevassemap imports FAILED - check you are in the right directory to import the crevassemap module from LFMapper")

def test_access_smooth():
	try:
		from crevassemap.smoothfft import smooth
	except:
		sys.exit("FATAL ERROR: smooth function can't be accessed - check access to crevassemap module")	

def test_plotting():
	try:
		import matplotlib.pyplot as plt
		x=[1,2,3,4]
		y=[1,2,3,4]
		plt.plot(x,y)
		plt.show()
		#plt.close()
	except:
		sys.exit("NON-FATAL ERROR: plotting not working - check you have x11 forwarding enabled")

##### Raster functions test
def test_98_load_envi_dimensions():
	
	envi_file_name = 'tests/TEST_DATA/helheim_hyperspec_subset.bin'
	image_array, post, (geotransform, inDs) = raster_functions.load_envi(envi_file_name)
	expect_cols = 1000.

	try:
		assert image_array.shape[0] == expect_cols
	except AssertionError:
		sys.exit("FATAL ERROR: ENVI file loading not working properly - array object different size to specified image dimensions\n -- check file and path is valid")
		

def test_99_load_envi_post():
	
	non_envi_file_name = 'tests/TEST_DATA/zebra.jpg'
	image_array, post, (geotransform, inDs) = raster_functions.load_envi(non_envi_file_name)
	non_envi_post = 1
	
	try:
		assert post == non_envi_post
	except AssertionError:
		sys.exit("FATAL ERROR: ENVI file loading not working properly - observed post different to expected post\n -- check file and path is valid")

##### Main Tests

from crevassemap import raster_functions, spacing, image_step_clean, plots

def test_plots():

	try:
		import numpy as np
		a=np.ones([3,3])
		envidata=False
		plots.plot_image(a, 'test', 'tests/test_output/TEST_PLOT', envidata, 1)
	except:
		sys.exit("FATAL ERROR: crevassemap.plots() failed")

def test_100_full_run_ENVI():

	try:

		envi_file_name = 'tests/TEST_DATA/helheim_hyperspec_subset.bin'
		output_dir = 'tests/test_output'
		expect_cols = 1000.
		expect_rows = 1000.

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
				spacing.find_spacings(img, date, kernel_size, stepsize, envidata, post, output_dir, spectrum_n, interact=False)

	except:
		sys.exit("FATAL ERROR: Main code has broken down using an ENVI file... consider changes since last commit")

def test_101_full_run_NON_ENVI():
		
	try:

		non_envi_file_name = 'tests/TEST_DATA/zebra.jpg'
		output_dir = 'tests/test_output'
		non_envi_cols = 518
		non_envi_rows = 386
		non_envi_post = 1

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
				spacing.find_spacings(img, date, kernel_size, stepsize, envidata, post, output_dir, spectrum_n, interact=False)

	except:
		sys.exit("FATAL ERROR: Main code has broken down using a NON-ENVI file... consider changes since last commit")


