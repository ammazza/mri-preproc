import os

home = os.path.expanduser("~")

### Atlas paths
atlas_dir = os.path.join(home, 'mri')
atlas_t1_path = os.path.join(atlas_dir, 'mni_icbm152_t1_tal_nlin_sym_09a.nii')
atlas_mask_path = os.path.join(atlas_dir, 'mni_icbm152_t1_tal_nlin_sym_09a_mask.nii')

### Only use centre-of-mass registration - For development
com_only = False
