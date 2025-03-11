import numpy as np
import numpy.typing as npt
from dipy.align.imaffine import (AffineRegistration, MutualInformationMetric, transform_centers_of_mass)
from dipy.align.transforms import (TranslationTransform3D, RigidTransform3D, AffineTransform3D)
import datetime

# Small utility function to print out registration timings.
def print_now(prefix=''):
    print(prefix, end='')
    print(datetime.datetime.now().time())

# ChatGPT: I chose dipy because I remember it was used in medpy and it had
# a very comprehensive tutorial, where I could easily find an example for my use case:
# https://docs.dipy.org/stable/examples_built/registration/affine_registration_3d.html
# The given example is clear in intent and exactly what I need, but it's complicated by
# showing 2 different APIs and by intermingled interactive visualisation code. So I asked
# ChatGPT to give me a simple function that would align two images, already available as ndarrays,
# using the same iterative refinement suggested in the documentation (i.e. start with centre of mass
# registration, then MI-based rigid, then rotations, then full affine).
# It produced some decent code with only a few errors (some wrong imports and misspelled keywords)
# that I easily fixed just with the help of the IDE (PyCharm).
def register_images(fixed: npt.NDArray[np.floating], moving: npt.NDArray[np.floating], com_only=False) -> npt.NDArray[np.floating]:
    """
    Registers the moving image to the fixed image using affine transformation.

    Parameters:
        fixed (np.ndarray): The reference (fixed) image.
        moving (np.ndarray): The image to be registered (moving).

    Returns:
        np.ndarray: The 4x4 affine transformation matrix.
    """
    # Define the similarity metric (Mutual Information)
    metric = MutualInformationMetric(nbins=32)

    # Define optimizer parameters
    level_iters = [10000, 1000, 100]  # Multi-resolution iterations
    # TODO: my understanding is the final step (100 iterations) will
    # use sigma 0 (no smoothing) and factor 1 (no downsampling), but double check.
    sigmas = [3.0, 1.0, 0.0]  # Smoothing levels
    factors = [4, 2, 1]  # Downsampling factors

    # Initialize Affine Registration framework
    affine_reg = AffineRegistration(metric=metric, level_iters=level_iters,
                                    sigmas=sigmas, factors=factors)

    # Step 1: Center of Mass Alignment (Coarse)
    print_now('Starting CoM: ')
    c_of_mass = transform_centers_of_mass(fixed, np.eye(4), moving, np.eye(4))
    result = c_of_mass

    # For development: make it possible to run CoM only, which is super fast.
    if not com_only:
        # Step 2: Translation Transformation
        print_now('Starting translation: ')
        translation = affine_reg.optimize(fixed, moving, TranslationTransform3D(), params0=None, starting_affine=c_of_mass.affine)

        # Step 3: Rigid Transformation (Rotation + Translation)
        print_now('Starting rigid: ')
        rigid = affine_reg.optimize(fixed, moving, RigidTransform3D(), params0=None, starting_affine=translation.affine)

        # Step 4: Full Affine Transformation (Scaling + Shearing + Rotation + Translation)
        print_now('Starting affine: ')
        affine = affine_reg.optimize(fixed, moving, AffineTransform3D(), params0=None, starting_affine=rigid.affine)
        result = affine

    print_now('Finished registration: ')
    return result
