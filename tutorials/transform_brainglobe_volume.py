import os

# os.chdir("..")
from brainglobe_atlasapi.bg_atlas import BrainGlobeAtlas
import CCF_translator


voxel_size_micron = 25
space_name = r"allen_mouse"
atlas = BrainGlobeAtlas(f"{space_name}_{voxel_size_micron}um")
source_age = 56
target_age = 32

CCFT_vol = CCF_translator.Volume(
    values=atlas.reference,
    space="allen_mouse",
    voxel_size_micron=voxel_size_micron,
    segmentation_file=False,
    age_PND=source_age,
)
CCFT_vol.transform(target_age, "demba_dev_mouse")
CCFT_vol.save(rf"demo_data/demba_P32_from_allen.nii.gz")

import os

# os.chdir("..")
from brainglobe_atlasapi.bg_atlas import BrainGlobeAtlas
import CCF_translator


voxel_size_micron = 20
space_name = r"princeton_mouse"
atlas = BrainGlobeAtlas(f"{space_name}_{voxel_size_micron}um")
source_age = 56
target_age = 56

CCFT_vol = CCF_translator.Volume(
    values=atlas.reference,
    space="princeton_mouse",
    voxel_size_micron=voxel_size_micron,
    segmentation_file=False,
    age_PND=source_age,
)
CCFT_vol.save(rf"demo_data/princeton_mouse_from_princeton.nii.gz")

CCFT_vol.transform(target_age, "allen_mouse")
CCFT_vol.save(rf"demo_data/allen_mouse_from_princeton.nii.gz")
