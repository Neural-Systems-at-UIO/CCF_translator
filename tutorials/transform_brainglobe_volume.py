import os 
os.chdir('..')
from brainglobe_atlasapi.bg_atlas import BrainGlobeAtlas
import CCF_translator


voxel_size_micron = 10
space_name = r"allen_mouse"
atlas = BrainGlobeAtlas("{space_name}_{voxel_size_micron}um")
source_age = 56
target_age= 32

CCFT_vol = CCF_translator.volume(
    values = atlas.reference,
    space = 'allen_mouse',
    voxel_size_micron=voxel_size_micron,
    segmentation_file=False,
    age_PND = source_age
)
CCFT_vol.transform(target_age, 'demba_dev_mouse')

CCFT_vol.save(rf"demo_data/P{target_age}_template_{voxel_size_micron}um.nii.gz")
