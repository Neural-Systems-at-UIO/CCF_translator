import numpy as np
from brainglobe_atlasapi.bg_atlas import BrainGlobeAtlas
from scipy.ndimage import zoom
import os

# test_data_dir = os.path.dirname(__file__)
test_data_dir = r"/home/harryc/github/CCF_translator/tests/test_data/"


test_atlas = BrainGlobeAtlas("allen_mouse_100um")
reference = zoom(test_atlas.reference, 0.5)
annotation = zoom(test_atlas.annotation, 0.5, order=0)
# Save the arrays using numpy with compression
np.savez_compressed(
    os.path.join(test_data_dir, "volumes", "allen_mouse_200um"),
    reference=reference,
    annotation=annotation,
)


test_atlas = BrainGlobeAtlas("princeton_mouse_20um")
reference = zoom(test_atlas.reference, 0.1)
annotation = zoom(test_atlas.annotation, 0.1, order=0)
# Save the arrays using numpy with compression
np.savez_compressed(
    os.path.join(test_data_dir, "volumes", "princeton_mouse_200um"),
    reference=reference,
    annotation=annotation,
)


# at present the latest gubra and demba atlases are not in brainglobe so we will load them manually
gubra_mri = r"/home/harryc/github/gubra/Multimodal_mouse_brain_atlas_files/MRI_space_oriented/mri_new_header.nii.gz"
gubra_mri_img = nib.load(gubra_mri).get_fdata()
