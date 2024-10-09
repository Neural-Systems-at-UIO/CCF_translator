# these lines are useful if you would like to use a git cloned ccf_translator. 
import os
import sys
sys.path.append(os.path.abspath("/home/harryc/github/CCF_translator/"))
import nibabel as nib
from CCF_translator import VolumeSeries, Volume
import os
import numpy as np


# # Usage example
VOXEL_SIZE_MICRON = 20
SPACE_NAME = "demba_dev_mouse"
DATA_FOLDER = "/home/harryc/github/demba_analysis/"
KEY_AGES = [56, 28, 14, 4]

volumes = []
for age in KEY_AGES:
    volume_path = os.path.join(DATA_FOLDER, f"P{age}_gene_vol_all.nii.gz")
    try:
        volume_data = nib.load(volume_path).get_fdata()
    except FileNotFoundError:
        print(f"File not found: {volume_path}")
        continue
    volume_data = volume_data[:,::-1,::-1] 
    volume_data = volume_data.transpose([0,2,1])
    volume = Volume(
        values=volume_data,
        space=SPACE_NAME,
        voxel_size_micron=VOXEL_SIZE_MICRON,
        segmentation_file=False,
        age_PND=age,
    )
    volumes.append(volume)
    

volume_series = VolumeSeries(volumes)
volume_series.interpolate_series()
volume_series.save(output_dir="/home/harryc/github/demba_analysis/interpolated_gene/")
