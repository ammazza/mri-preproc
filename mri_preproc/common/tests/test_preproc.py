import numpy as np
import mri_preproc.common.preproc as preproc

# Overly simple test examples.
# TODO: a lot! First, factor out the test inputs as fixtures
#  and create them only once per suite.

def test_normalise_min_max_preserves_shape():
    ones_img = ones_array = np.ones((4, 4, 4))
    output = preproc.normalise_min_max(ones_img)
    # Check normalisation preserves shape.
    assert ones_img.shape == output.shape

def test_normalise_min_max_single_value():
    ones_img = ones_array = np.ones((4, 4, 4))
    output = preproc.normalise_min_max(ones_img)
    # Check normalisation of a single value returns all zeros.
    assert np.isclose(np.min(output), 0.0) and np.isclose(np.max(output), 0.0)
