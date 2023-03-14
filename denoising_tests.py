"""
This script will take a dataset and test several different denoising algoirthms
on it, including:

Gaussian
Total variation filter
Wavelet denoising filter
Non-Local Means
BM3D Block-matching and 3D filtering

Where possible, different parameter values will also be tested.
Alot of this code was fro:

Author: Dr. Sreenivas Bhattiprolu
https://github.com/bnsreenu/python_for_microscopists/blob/master/094_denoising_MRI.py

"""

from skimage import io, img_as_float, img_as_ubyte
import cv2

noisy_img_org = io.imread("Test_slize24_green.tif")
noisy_img = img_as_float(noisy_img_org)
noisy_img_ubyte = img_as_ubyte(noisy_img_org)

print("Image import complete!")

####################GAUSSIAN DENOISING####################
from scipy import ndimage as nd

print("Running Gaussian Denoising...")

# Sigma values to be screened
sigmas = [0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3]

for sigma in sigmas:
    gaussian_img = nd.gaussian_filter(noisy_img, sigma=sigma)
    gaussian_filename = "gaussian_sigma_" + str(sigma) + ".tif"
    gaussian_img_8bit = cv2.normalize(gaussian_img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    io.imsave(gaussian_filename, img_as_ubyte(gaussian_img_8bit))


####################TV AND WAVELET DENOISING####################
from skimage.restoration import (denoise_tv_chambolle, denoise_wavelet, estimate_sigma)

print("Running TV Denoising...")

#TV denoising weights to screen
TV_weights = [0.01, 0.05, 0.1, 0.25, 0.5, 1, 2, 5]

for tv in TV_weights:
    denoise_TV = denoise_tv_chambolle(noisy_img, weight=tv, multichannel=False)
    tv_filename = "tv_weight_" + str(tv) + ".tif"
    tv_img_8bit = cv2.normalize(denoise_TV, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    io.imsave(tv_filename, tv_img_8bit)

print("Running Wavelet Denoising...")

#Wavelet
wavelet_smoothed = denoise_wavelet(noisy_img, multichannel=False,
                           method='BayesShrink', mode='soft',
                           rescale_sigma=True)
wavelet_img_8bit = cv2.normalize(wavelet_smoothed, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
io.imsave("Wavelet.tif", wavelet_img_8bit)

####################MEDIAN DENOISING####################
from skimage.filters import median
from skimage.morphology import disk

print("Running Median Denoising...")

disc_values = [0, 1, 2, 3, 4, 5]

for disc in disc_values:
    median_img = median(noisy_img_ubyte, disk(disc), mode='constant', cval=0.0)
    disc_filename = "Median_disk_" + str(disc) + ".tif"
    median_img_8bit = cv2.normalize(median_img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    io.imsave(disc_filename, median_img_8bit)


####################NON-LOCAL MEANS DENOISING####################
from skimage.restoration import denoise_nl_means
from skimage import img_as_ubyte, img_as_float
import numpy as np

print("Running Non-Local Means Denoising...")

sigma_est = np.mean(estimate_sigma(noisy_img, multichannel=False))

patch_sizes = [3, 9, 15]
patch_distances = [2, 5, 10]

for size in patch_sizes:
    for dist in patch_distances:
        NLM_img = denoise_nl_means(noisy_img, h=1.15 * sigma_est, fast_mode=False,
                                       patch_size=9, patch_distance=5, multichannel=False)
        NLM_filename = "NLM_size_" + str(size) + "_dist_" + str(dist) + ".tif"
        NLM_img_8bit = cv2.normalize(NLM_img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        io.imsave(NLM_filename, NLM_img_8bit)


####################BLOCK-MATCHING AND 3D FILTERING####################
import bm3d
import numpy as np

print("Running Block-matching and 3D filtering Denoising...")

sigma_psds = [0, 0.01, 0.05, 0.1, 0.2, 0.5, 1]

for psd in sigma_psds:
    ALL_STAGES_img = bm3d.bm3d(noisy_img, sigma_psd=psd, stage_arg=bm3d.BM3DStages.ALL_STAGES)
    ALL_STAGES_filename = "BM3D_ALL_psd_" + str(psd) + ".tif"
    ALL_STAGES_img_8bit = cv2.normalize(ALL_STAGES_img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    io.imsave(ALL_STAGES_filename, ALL_STAGES_img_8bit)

for psd in sigma_psds:
    HARD_img = bm3d.bm3d(noisy_img, sigma_psd=psd, stage_arg=bm3d.BM3DStages.HARD_THRESHOLDING)
    HARD_filename = "BM3D_HARD_psd_" + str(psd) + ".tif"
    HARD_img_8bit = cv2.normalize(HARD_img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    io.imsave(HARD_filename, HARD_img_8bit)
