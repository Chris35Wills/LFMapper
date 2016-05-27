import sys
import matplotlib.pyplot as plt
from crevassemap import raster_functions, spacing, image_step_clean

interact=False # if True shows images - will fail if x11 forwarding not set

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

### DATA SPEC
envi_file_name = 'tests/TEST_DATA/helheim_hyperspec_subset.bin'
output_dir = 'tests/test_output'
expect_cols = 1000.
expect_rows = 1000.

### MAIN RUN
step_range = ([101])#([3])
kernel_range = ([9])#([3])

check_odd_kernel(kernel_range[0])
check_odd_step(step_range[0])

flag = "GLACIER_ENVI"
spectrum_n = 1.5 ## noise value (2 = brown)

image_array, post, envidata = raster_functions.load_envi(envi_file_name)

#plot input image
if interact:
	plt.imshow(image_array)
	plt.title("input ENVI")
	plt.show(block=False)

for stepsize in step_range:
	for kernel_size in kernel_range:
		img = image_step_clean.image_step_clean(stepsize, image_array)
		spacing.find_spacings(img, flag, kernel_size, stepsize, envidata, post, output_dir, spectrum_n, interact=interact)

print("\n ENVI EXAMPLE COMPLETE\n")
print("\n Data saved: %s \n" %output_dir)
