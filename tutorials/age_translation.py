import CCF_translator as CCFT
import nibabel as nib
import numpy as np

# Load the image
image_P31 = nib.load("demo_data/DeMBA_P56_brain_mod.nii.gz")
volume_P31 = image_P31.get_fdata()
# Create a CCFT object
# this can be done for either volumes or points
# for volumes we would run the following
CCFT_vol = CCFT.volume(data=volume_P31, space="CCFv3", voxel_size_micron=20, age_PND=31)


# alternatively for points we could do this
with open("my_points.txt") as f:
    points = np.array(f.readlines())
CCFT_pts = CCFT.create_pointset(points, space="CCFv3", voxel_size_micron=20, age_PND=31)

# we can then translate either the points or volumes into a new target age or space.
# CCFT will try to find a path from the current space into the target one
CCFT_vol.translate(target_age=56)
# the API is the same for points
CCFT_pts.translate(target_age=56)

# To check the current age of any CCFT object run
print(CCFT_vol.current_age)  # -> P56
# To check the original age of any object run
print(CCFT_vol.original_age)  # -> P31
