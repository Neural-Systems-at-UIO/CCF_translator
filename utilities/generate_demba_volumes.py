import os
# os.chdir('..')
from brainglobe_atlasapi.bg_atlas import BrainGlobeAtlas
import CCF_translator
import nibabel as nib
import numpy as np


"""
The following code projects the Allen annotations and template at 10um
down to the DeMBA ages.  
"""
voxel_size_micron = 10
space_name = r"allen_mouse"
start_age = 56
youngest_age = 4
save_path = rf"/home/harryc/Downloads/demba_{voxel_size_micron}um"
"""atlas = BrainGlobeAtlas(f"{space_name}_{voxel_size_micron}um")

for end_age in range(start_age, youngest_age-1,  -1):
    print(f"processing age: {end_age}")
    CCFT_vol = CCF_translator.volume(
        values = atlas.reference,
        space = 'allen_mouse',
        voxel_size_micron=voxel_size_micron,
        segmentation_file=False,
        age_PND = start_age
    )
    CCFT_vol.transform(end_age, 'demba_dev_mouse')
    CCFT_vol.save(rf"{save_path}/P{end_age}_template_{voxel_size_micron}um.nii.gz")
    CCFT_vol = CCF_translator.volume(
        values = atlas.annotation,
        space = 'allen_mouse',
        voxel_size_micron=voxel_size_micron,
        segmentation_file=False,
        age_PND = start_age
    )
    CCFT_vol.transform(end_age, 'demba_dev_mouse')
    CCFT_vol.save(rf"{save_path}/P{end_age}_annotation_{voxel_size_micron}um.nii.gz")
"""

"""
The following code creates the intermediate datasets between the ages
"""
voxel_size_micron = 20
space_name = "demba_dev_mouse"
data_folder = "/mnt/z/HBP_Atlasing/Developmental_atlases/DeMBA_Developmental mouse brain atlas/DeMBA-v1/01_working-environment/01_Data/DeMBA_v1/interpolated_templates/"
key_ages = [56, 28, 21, 14, 7, 4]

for i in range(len(key_ages) - 1):
    older_age = key_ages[i]
    younger_age = key_ages[i+1] 
    older_img = nib.load(rf"{data_folder}/DeMBA_P{older_age}_brain.nii.gz")
    older_volume = np.asanyarray(older_img.dataobj)
    younger_img = nib.load(rf"{data_folder}/DeMBA_P{younger_age}_brain.nii.gz")
    younger_volume = np.asanyarray(younger_img.dataobj)
    for age in range(younger_age, older_age):
        CCFT_young = CCF_translator.volume(
        values = younger_volume,
        space = space_name,
        voxel_size_micron=voxel_size_micron,
        segmentation_file=False,
        age_PND = younger_age
        )
        CCFT_old = CCF_translator.volume(
        values = older_volume,
        space=space_name,
        voxel_size_micron=voxel_size_micron,
        segmentation_file=False, 
        age_PND=older_age
        )   
        if age!=older_age:
            CCFT_young.transform(target_age=age, target_space=space_name)
        if age!=younger_age:
            CCFT_old.transform(target_age=age, target_space=space_name)
        young_factor = ((older_age-younger_age) / (older_age - age))
        old_factor = 1 - young_factor
        CCFT_young.values *= young_factor
        CCFT_old.values *= old_factor
        average = (CCFT_young.values + CCFT_old.values).astype(np.uint8)
        average_volume = CCF_translator.volume(
            values = average,
            space = space_name,
            voxel_size_micron = voxel_size_micron,
            segmentation_file = False,
            age_PND = age
        )
        average_volume.save(f"demo_data/DeMBA_P{age}.nii.gz")

