import numpy as np

def flatten_spectrum(spec, n=2):
	"""Flatten an FFT spectrum with a given power law, and trim it."""
	spec = np.abs(spec)
	spec = np.fft.fftshift(spec)
	u, v = spec.shape
	x, y = np.meshgrid(np.arange(-(u//2), u-u//2), np.arange(-(v//2), v-v//2))
	r = (x ** 2 + y ** 2) ** 0.5
	spec = spec * r ** n
	return spec

if __name__ == "__main__":
	print("Run from import.")