from brainglobe_atlasapi.bg_atlas import BrainGlobeAtlas
import CCF_translator



"""
The following code projects the Allen annotations and template at 10um
down to the DeMBA ages.  
"""
voxel_size_micron = 10
space_name = r"allen_mouse"
atlas = BrainGlobeAtlas("{space_name}_{voxel_size_micron}um")
start_age = 56
save_path = rf"/home/harryc/Downloads/demba_{voxel_size_micron}um"

for end_age in range(start_age, 4-1,  -1):
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
The following code creates the intermediate datasets between the ages
"""