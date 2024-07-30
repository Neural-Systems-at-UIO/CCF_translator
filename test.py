"""import CCF_translator
import nibabel as nib
import numpy as np
import networkx as nx
image_path = r"demo_data/DeMBA_P56_brain.nii.gz"
img = nib.load(image_path) 
data = np.asanyarray(img.dataobj)


CCFT_vol = CCF_translator.volume(
    values = data,
    space = 'Demba',
    voxel_size_um=20,
    segmentation_file=False,
    age_PND = 56
)


CCFT_vol.transform(56, 'Allen_CCFv3')


save_volume( CCFT_vol, 'Allen_CCFv3_template_testing_save.nii.gz')

print('finished saving template')"""
import CCF_translator
import nibabel as nib
import numpy as np
import networkx as nx
def save_volume(CCFT_vol, save_path):
    vol_metadata = {"space":CCFT_vol.space,
                    "age_PND":CCFT_vol.age_PND,
                    "segmentation_file":CCFT_vol.segmentation_file}
    affine = np.eye(4) 
    affine[:3,:3] *= CCFT_vol.voxel_size_um
    image = nib.Nifti1Image(CCFT_vol.values, affine=affine)
    image.header["descrip"] = vol_metadata
    image.header.set_xyzt_units(3)
    nib.save(image, save_path)

image_path = r"demo_data/DeMBA_P28_brain.nii.gz"
img = nib.load(image_path) 
data = np.asanyarray(img.dataobj)


CCFT_vol = CCF_translator.volume(
    values = data,
    space = 'Demba',
    voxel_size_um=20,
    segmentation_file=False,
    age_PND = 28
)


CCFT_vol.transform(56, 'Allen_CCFv3')


save_volume( CCFT_vol, 'Allen_CCFv3_testing_save.nii.gz')
"""

print('finished saving template')
import CCF_translator
import nibabel as nib
import numpy as np
import networkx as nx
image_path = r"demo_data/DeMBA_P28_brain.nii.gz"
img = nib.load(image_path) 
data = np.asanyarray(img.dataobj)


CCFT_vol = CCF_translator.volume(
    values = data,
    space = 'Demba',
    voxel_size_um=20,
    segmentation_file=False,
    age_PND = 28
)


CCFT_vol.transform(56, 'Demba')


save_volume( CCFT_vol, 'Demba_28_to_56_testing_save.nii.gz')"""
"""TODO 
transform points
"""
"""
if you wanted to get the voxel size from the header you could do so like this
voxel_size = img.header['pixdim']
unit = img.header['xyzt_units'][1]
if unit==1:
    voxel_size *= 1e6
if unit==2:
    voxel_size *= 1e3
"""