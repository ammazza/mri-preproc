import numpy as np
import numpy.typing as npt
from scipy.ndimage import gaussian_filter

# ChatGPT: I gave it my intended signature to check the correct way of specifying floating
# point values in the type hint, i.e. "img: np.ndarray[???]" - And before I could ask it gave
# me the full implementation, lol. Anyway, I wasn't aware of the following:
# "...mypy doesn't fully support np.ndarray[...] yet, so use npt.NDArray[np.floating] from numpy.typing"
def normalise_min_max(img: npt.NDArray[np.floating]) -> npt.NDArray[np.floating]:
    """Given an image return a min-max normalised version of it. The input isn't modified.

    Parameters:
        img (npt.NDArray[np.floating]): Input image as a NumPy array with floating-point values.

    Returns:
        npt.NDArray[np.floating]: Min-max normalised image as a new NumPy array.
    """
    min_val = img.min()
    max_val = img.max()

    # Corner case: the image contains the same value in all voxels. It gets
    # correctly normalised to all zeros and we prevent division by zero.
    if max_val == min_val:
        return np.zeros_like(img, dtype=np.float32)

    return (img - min_val) / (max_val - min_val)

# ChatGPT: I remembered SciPy had a gaussian filter function which takes a kernel size, but also
# has a bunch of additional parameters, in particular about handling the image borders. Rather
# than reading through the SciPy docs I asked for an example with an explanation of all major
# parameters. After reviewing it I decided I was happy with the defaults.
#
# TODO: while sigma is a float, it is expressed in voxels. It should be decided/clarified if the
# calling code should use the image's real world units (i.e. voxel size) to express the sigma in mm.
def apply_gaussian_smoothing(img: npt.NDArray[np.floating], sigma: float) -> npt.NDArray[np.floating]:
    """
    Applies Gaussian smoothing to the given image.

    Parameters:
        img (npt.NDArray[np.floating]): Input image as a NumPy array with floating-point values.
        sigma (float): Standard deviation for Gaussian kernel.

    Returns:
        npt.NDArray[np.floating]: Smoothed image.
    """
    # Defaults are truncate at 4*sigma and 'reflect' image edges, which
    # is fine because the important info is at the centre and we expect
    # mostly black edges.
    return gaussian_filter(img, sigma=sigma)
