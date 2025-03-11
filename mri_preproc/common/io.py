import numpy as np
import numpy.typing as npt
import nibabel as nib
from typing import Callable
from mri_preproc.common.preproc import (normalise_min_max, apply_gaussian_smoothing)

# TODO: it would be good to standardise the application to one image representation
# that has all the info but abstracts the source format. ITK types could be a good
# candidate or a custom class wrapping the necessary info. Here I approximate the
# latter with a dictionary: {image: voxel-data, transform: affine-RAS-transform}.
def load_nifti(
    path: str,
    normf: Callable[[npt.NDArray[np.floating]], npt.NDArray[np.floating]] = None,
    sigma: float = 0.0
    ) -> dict[str, npt.NDArray[np.floating]]:
    """TODO"""
    # TODO: I/O error handling + validation
    img = nib.load(path)
    print(f'Loaded image: {path}')
    print(f'- Dimensions: {img.header['dim']}')
    print(f'- Voxel size: {img.header['pixdim']}')

    # TODO: some validation - e.g. is it a 3D image, are the units supported, etc.

    # Extract the image data and, if requested, preprocess it.
    img_data = img.get_fdata()
    if normf is not None:
        img_data = normf(img_data)
    if sigma > 0:
        img_data = apply_gaussian_smoothing(img_data, sigma)

    # Extract the image RAS+ transformation
    img_trans = img.affine

    return { 'image': img_data,
             'transform': img_trans }

def save_nifti(path: str, img: dict[str, npt.NDArray[np.floating]]):
    # TODO: I/O error handling, valid format, etc.
    output = nib.Nifti1Image(img['image'], img['transform'])
    print(f'Saving nifti image to: {path}')
    nib.save(output, path)
