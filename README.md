# mri-preproc

A library and CLI tool to preprocess T1-weighed head MRI scans 
in NIfTI format and extract the brain.

## Quickstart

This section will help you install and test-run `mri-preproc`.

### Installing atlas and example data

To function correctly `mri-preproc` needs some atlas data.
Complete the following steps to set up the machine running `mri-preproc`.

- In your home directory create a folder named `mri` (see below for configuration)
- Download the [ICBM 2009a Nonlinear Symmetric Atlas](http://www.bic.mni.mcgill.ca/~vfonov/icbm/2009/mni_icbm152_nlin_sym_09a_nifti.zip)
- Unzip the atlas data into `~/mri` so that the individual nifti files are in `~/mri` 

__Note on configuration:__ the atlas directory and file names are defined in [this config file](mri_preproc/brain_extract/config.py).
If you want to use a different atlas setup, adjust the atlas variables accordingly.

To try `mri-preproc` you will need a T1-weighted head scan in NIfTI format.
For the sake of example download [this MRI scan](https://s3.amazonaws.com/openneuro.org/ds000247/sub-0002/ses-01/anat/sub-0002_ses-01_T1w.nii.gz?versionId=71.XAnuxtjw6ITyFLSPZeH_lAayTeyvq)
in the `~/mri` folder created above.

### Installing dependencies with uv

`mri-preproc` was developed using `uv` to manage python versions and dependencies.
If you don't have `uv` already installed, please follow the instructions on
[the official GitHub repo](https://github.com/astral-sh/uv).

After you have `uv` installed, you can install `mri-preproc` dependencies and
create a virtual environment for it, by running the following command in the
repository root:

```bash
uv sync
```

### Installing dependencies with pip

TODO: use `uv` to generate `requirements.txt` and provide instructions.

### Running mri-preproc

Once the necessary data and dependencies are installed, run the following
commands in the repository root:

```bash
# Activate the virtual environment with the correct python and libs 
source .venv/bin/activate

# Run mri-proc on the example MRI scan 
python -m mri_preproc.main --input ~/mri/sub-0002_ses-01_T1w.nii.gz --output ~/mri/output.nii.gz --sigma 2

# For help with mri-proc parameters invoke:
python -m mri_preproc.main --help
```

__Note__: a single run can take several minutes (because of the registration
step). When developing or experimenting set `com_only = True` in [this config file](mri_preproc/brain_extract/config.py).
That will limit registration to centre-of-mass alignment, which too low quality for any real-world use
but extremely fast.

## Design and caveats



