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
down to the DeMBA ages.  
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
    CCFT_vol = CCF_translator.volume(
        values=allen_atlas.reference,
        space="allen_mouse",
        voxel_size_micron=voxel_size_micron,
        segmentation_file=False,
        age_PND=start_age,
    )
    CCFT_vol.transform(end_age, "demba_dev_mouse")
    CCFT_vol.save(rf"{save_path}/P{end_age}_template_{voxel_size_micron}um.nii.gz")
    CCFT_vol = CCF_translator.volume(
        values=allen_atlas.annotation,
        space="allen_mouse",
        voxel_size_micron=voxel_size_micron,
        segmentation_file=True,
        age_PND=start_age,
    )
    CCFT_vol.transform(end_age, "demba_dev_mouse")
    CCFT_vol.save(rf"{save_path}/P{end_age}_annotation_{voxel_size_micron}um.nii.gz")
    CCFT_vol = CCF_translator.volume(
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


"""
The following code creates the intermediate templates between the ages
"""
voxel_size_micron = 20
space_name = "demba_dev_mouse"
data_folder = "/mnt/z/HBP_Atlasing/Developmental_atlases/DeMBA_Developmental mouse brain atlas/DeMBA-v1/01_working-environment/01_Data/DeMBA_v1/interpolated_templates/"
key_ages = [56, 28, 21, 14, 7, 4]

for i in range(len(key_ages) - 1):
    older_age = key_ages[i]
    younger_age = key_ages[i + 1]
    older_img = nib.load(rf"{data_folder}/DeMBA_P{older_age}_brain.nii.gz")
    older_volume = np.asanyarray(older_img.dataobj)
    younger_img = nib.load(rf"{data_folder}/DeMBA_P{younger_age}_brain.nii.gz")
    younger_volume = np.asanyarray(younger_img.dataobj)
    for age in range(younger_age, older_age + 1):
        CCFT_young = CCF_translator.volume(
            values=younger_volume.copy(),
            space=space_name,
            voxel_size_micron=voxel_size_micron,
            segmentation_file=False,
            age_PND=younger_age,
        )
        CCFT_old = CCF_translator.volume(
            values=older_volume.copy(),
            space=space_name,
            voxel_size_micron=voxel_size_micron,
            segmentation_file=False,
            age_PND=older_age,
        )
        if age != older_age:
            CCFT_young.transform(target_age=age, target_space=space_name)
        if age != younger_age:
            CCFT_old.transform(target_age=age, target_space=space_name)

        young_factor = (older_age - age) / (older_age - younger_age)
        old_factor = 1 - young_factor
        print(age)

        CCFT_young.values *= young_factor
        CCFT_old.values *= old_factor
        new_data = CCFT_young.values + CCFT_old.values
        print("new_data")
        print(new_data.max())
        print(new_data.min())
        average = (new_data).astype(np.uint8)
        average_volume = CCF_translator.volume(
            values=average,
            space=space_name,
            voxel_size_micron=voxel_size_micron,
            segmentation_file=False,
            age_PND=age,
        )
        outname = f"demo_data/demba_vols/DeMBA_P{age}.nii.gz"
        print(f"saving as outname {outname}")
        average_volume.save(outname)


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
    CCFT_vol = CCF_translator.volume(
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
