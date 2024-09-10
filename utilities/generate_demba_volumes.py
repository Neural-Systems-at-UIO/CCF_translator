import os

# os.chdir('../..')
import sys

sys.path.append(os.path.abspath("/home/harryc/github/CCF_translator/"))
import os
from brainglobe_atlasapi.bg_atlas import BrainGlobeAtlas
import CCF_translator as CCF_translator
import nibabel as nib
import numpy as np


"""
The following code projects the Allen annotations and template at 10um
down to the DeMBA ages.  If you would like to see how the interpolated 
DeMBA templates are generated please see the create_series file in the 
same folder as this script.
"""
voxel_size_micron = 10
allen_space_name = r"allen_mouse"
kim_space_name = r"kim_dev_mouse_stp"
start_age = 56
youngest_age = 4
save_path = rf"demo_data/demba_{voxel_size_micron}um"
allen_atlas = BrainGlobeAtlas(f"{allen_space_name}_{voxel_size_micron}um")
kim_atlas = BrainGlobeAtlas(f"{kim_space_name}_{voxel_size_micron}um")

t_start_age = 56
for end_age in range(t_start_age, youngest_age - 1, -1):
    print(f"processing age: {end_age}")
    CCFT_vol = CCF_translator.Volume(
        values=allen_atlas.reference,
        space="allen_mouse",
        voxel_size_micron=voxel_size_micron,
        segmentation_file=False,
        age_PND=start_age,
    )
    CCFT_vol.transform(end_age, "demba_dev_mouse")
    CCFT_vol.save(rf"{save_path}/P{end_age}_template_{voxel_size_micron}um.nii.gz")
    CCFT_vol = CCF_translator.Volume(
        values=allen_atlas.annotation,
        space="allen_mouse",
        voxel_size_micron=voxel_size_micron,
        segmentation_file=True,
        age_PND=start_age,
    )
    CCFT_vol.transform(end_age, "demba_dev_mouse")
    CCFT_vol.save(rf"{save_path}/P{end_age}_annotation_{voxel_size_micron}um.nii.gz")
    CCFT_vol = CCF_translator.Volume(
        values=kim_atlas.annotation,
        space="allen_mouse",
        voxel_size_micron=voxel_size_micron,
        segmentation_file=True,
        age_PND=start_age,
    )
    CCFT_vol.transform(end_age, "demba_dev_mouse")
    CCFT_vol.save(
        rf"{save_path}/P{end_age}_kim_annotation_{voxel_size_micron}um.nii.gz"
    )




import nrrd
import requests
import io
import tempfile

t_start_age = 56
volume_url = r"http://download.alleninstitute.org/informatics-archive/current-release/mouse_ccf/annotation/ccf_2022/annotation_10.nrrd"
response = requests.get(volume_url)
allen_2022_content = response.content

# Write the content to a temporary file
with tempfile.NamedTemporaryFile(delete=False) as temp_file:
    temp_file.write(allen_2022_content)
    temp_file_path = temp_file.name

# Read the NRRD file from the temporary file
allen_2022_array, header = nrrd.read(temp_file_path)
allen_2022_array.shape

for end_age in range(t_start_age, youngest_age - 1, -1):
    print(f"processing age: {end_age}")
    allen = allen_2022_array.copy()
    CCFT_vol = CCF_translator.Volume(
        values=allen,
        space="allen_mouse",
        voxel_size_micron=voxel_size_micron,
        segmentation_file=True,
        age_PND=start_age,
    )
    CCFT_vol.transform(end_age, "demba_dev_mouse")
    CCFT_vol.save(
        rf"{save_path}/P{end_age}_allen_2022_annotation_{voxel_size_micron}um.nii.gz"
    )
