from brainglobe_atlasapi.bg_atlas import BrainGlobeAtlas
import CCF_translator
import nrrd
#import matplotlib.pyplot as plt
atlas = BrainGlobeAtlas("allen_mouse_25um")


start_age = 56
end_age = 28

CCFT_vol = CCF_translator.volume(
    values = atlas.reference,
    space = 'Allen_CCFv3',
    voxel_size_um=25,
    segmentation_file=False,
    age_PND = start_age
)

CCFT_vol.transform(end_age, 'Demba')
CCFT_vol.save(rf"demo_data/P{end_age}_template_from_bgappi_Demba.nii.gz")
