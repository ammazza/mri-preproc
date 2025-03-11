import numpy as np
import numpy.typing as npt
from mri_preproc.registration.registration import register_images
# For development, set com_only registration to True
from mri_preproc.brain_extract.config import com_only

def extract_brain(
        original_image: npt.NDArray[np.floating],
        preproc_image: npt.NDArray[np.floating],
        atlas_image: npt.NDArray[np.floating],
        atlas_mask: npt.NDArray[np.floating]):
    """TODO"""

    # Register the input image (fixed) to the atlas reference image (moving).
    affine = register_images(preproc_image, atlas_image, com_only=com_only)

    # Use the result to transform the brain mask.
    # Checked docs for dipy.align.imaffine.AffineMap for interpolation:
    # default is 'linear', but also supports 'nearest', which is what we want
    # for a binary mask. Adding some assertions to check the mask is binary and
    # remains binary after transformation.
    # TODO: really, we should check the mask has 0 and 1 only.
    assert len(np.unique(atlas_mask)) == 2
    transformed_mask = affine.transform(atlas_mask, interpolation='nearest')
    assert len(np.unique(transformed_mask)) == 2

    # numpy array multiplication operator works element-wise, so multiplying
    # the image by the binary mask extracts the region of interest (brain).
    brain_image = original_image * transformed_mask

    return brain_image
