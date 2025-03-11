from mri_preproc.brain_extract.config import (atlas_t1_path, atlas_mask_path)
from mri_preproc.brain_extract.brain_extract import extract_brain
from mri_preproc.common.io import load_nifti, save_nifti
from mri_preproc.common.preproc import (normalise_min_max, apply_gaussian_smoothing)
import click

# ChatGPT: I didn't remember off the top of my head how to specify
# click options, so I gave ChatGPT the command line example from the
# coding challenge text and got it to write it for me.
@click.command()

@click.option(
    "--input",
    help="Path to the input T1 scan",
    type=click.Path(exists=True, dir_okay=False),
    required=True)

@click.option(
    "--output",
    help="Path of the output file to be created",
    type=click.Path(dir_okay=False),
    required=True)

@click.option(
    "--sigma",
    help="Sigma of the smoothing Gaussian kernel (in voxels)",
    type=float,
    required=True)

def process_mri(input, output, sigma):
    """
    Extract the brain from an MRI head scan.
    """
    click.echo(f"Processing: {input}")
    click.echo(f"Saving output to: {output}")
    click.echo(f"Applying Gaussian smoothing with sigma: {sigma}")

    # TODO: warn if sigma is not > 0

    # Load the original image and keep it as it is.
    input_image = load_nifti(input)

    # Load it again and perform preprocessing for registration.
    preproc_image = load_nifti(input, normalise_min_max, sigma)

    # Load the atlas reference image and preprocess it.
    # Note: it is questionable whether we want to smooth the atlas image,
    # since it is an average image and is already less sharp than a normal scan.
    atlas_image = load_nifti(atlas_t1_path, normalise_min_max, sigma)

    # Load the atlas brain mask.
    mask_image = load_nifti(atlas_mask_path)

    # Extract the brain from the original, unprocessed image.
    brain = extract_brain(
        input_image['image'],
        preproc_image['image'],
        atlas_image['image'],
        mask_image['image'])

    # TODO: it occurred to me only later that we're not explicitly
    # assigning any metadata to the NIfTI (except the RAS transform). For instance
    # we're not providing voxel sizes! Ooops. Definitely a bug to fix.
    save_nifti(output, {'image': brain, 'transform': input_image['transform']})

# source .venv/bin/activate
# python mri_preproc/main.py --help
# python mri_preproc/main.py --input ~/mri/sub-0002_ses-01_T1w.nii.gz --output ~/mri/output.nii.gz --sigma 2
if __name__ == "__main__":
    process_mri()
