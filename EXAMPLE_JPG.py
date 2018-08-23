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
non_envi_file_name = 'tests/TEST_DATA/zebra.jpg'

output_dir = 'tests/test_output'

non_envi_cols = 518
non_envi_rows = 386
non_envi_post = 1		

### MAIN RUN
step_range = ([1,3,5,7]) 
kernel_range = ([3])

	# NOTE THAT A STEPSIZE OF 1 (i.e. every cell) will leave a gap at the bottom and right margins - this is 
	# due to the effect of stepping into the image (by half the kernel - 1) to ensure all cells within the kernel 
	# are within the iamge. When it reaches the bottom corner, cells where the kernel is focused but where part of 
	# the kernel falls outside of the image are given NA values


check_odd_kernel(kernel_range[0])
check_odd_step(step_range[0])

flag = "ZEBRA_JPG"
spectrum_n = 1.5 ## noise value (2 = brown)

image_array, post, envidata = raster_functions.load_envi(non_envi_file_name)

#plot input image
if interact:
	plt.imshow(image_array)
	plt.title("input JPG")
	plt.show()

for stepsize in step_range:
	for kernel_size in kernel_range:
		img = image_step_clean.image_step_clean(stepsize, image_array)
		spacing.find_spacings(img, flag, kernel_size, stepsize, envidata, post, output_dir, spectrum_n, interact=interact)

print("\n JPG EXAMPLE COMPLETE\n")
print("\n Data saved: %s \n" %output_dir)
