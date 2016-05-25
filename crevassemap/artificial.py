from __future__ import division
import numpy as np
import os

import util


# size = 1 side of a square (px)
# angle = radians ("0" is at 3 o'clock) - represents orientation
# wavelength = wavelength (spacing) in px
# All noise created with SD of 1 = scale up if you want a larger range 
#	e.g. 10 * pink_noise(100) # gives pink noise of standard deviation 
#   10 over a 100x100 image (must be same size as the wave over which the noise is calculated)
# Too large an sd will result in the noise not being clear - noise is all over the place therefore signal is swamped
# All waves have a range -1:1

# We want to approximate the error in estimated spacings and orientations for signal with known noise

# range of wavelengths and angles to varying degrees of noise


def xygrid(size):
    y, x = np.mgrid[:size, :size]
    return x, y

def sloped(size, angle, slope=1.0):
    x, y = xygrid(size)
    return slope * (x * np.cos(angle) + y * np.sin(angle))

def sine_wave(size, angle, wavelength):
    return np.sin(sloped(size, angle, 2 * np.pi/wavelength))

def square_wave(size, angle, wavelength):
    slope = sloped(size, angle, 2/wavelength)
    return np.where(slope % 2 > 1, 1, -1)

def sawtooth_wave(size, angle, wavelength):
    slope = sloped(size, angle, 2/wavelength)
    return 2 * np.abs((slope % 2) - 1) - 1

def white_noise(size):
    return np.random.randn(size, size)

def coloured_noise(size, n):
    white = white_noise(size)
    fft = np.fft.fft2(white)
    x, y = xygrid(size)
    x[x > size // 2] -= size
    y[y > size // 2] -= size
    r2 = x ** 2 + y ** 2
    r2[0,0] = 1
    scaled_fft = fft / r2 ** (n/2)
    scaled_fft[0,0] = 0
    noise = np.fft.ifft2(scaled_fft).real
    return noise / np.std(noise)

def brown_noise(size):
    return coloured_noise(size, 2)

def pink_noise(size):
    return coloured_noise(size, 1)

def rms(x):
    return (x ** 2).mean() ** 0.5

def write_stats(filename, spacings, orientations, wavelength, snrs, wave_type, noise_type, noise_scale):
	util.check_output_dir(filename)
	if os.path.exists(filename):
		f = open(filename, 'a')
	else:
		f = open(filename, 'w')
		#f.write("Run, RMS spacing approx vs obs, spacing mean, RMS orientations, SnR mean\n")
		f.write("wave_type, noise_type, noise_scale, wavelength,  RMS spacing approx. vs obs, spacing mean, RMS orientations, SnR mean\n")
	f.write("%s, %s, %s, %s, %f, %f, %f, %f\n" %(wave_type, noise_type, noise_scale, wavelength, rms(spacings - wavelength), spacings.mean(), rms(orientations), snrs.mean() ))
	f.close()
	print "Stats file: %s" %(filename)

## If artificial.py is run at command line then __name__ == __main__
## If imported as a module, then __name__ != __main__
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    plt.imshow(sawtooth_wave(100, np.pi/4, 10) + 10 * pink_noise(100))
    plt.colorbar()
    plt.show()