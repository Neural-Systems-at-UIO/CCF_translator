import os
import sys
sys.path.append(os.path.abspath("/home/harryc/github/CCF_translator/"))
import nibabel as nib
from CCF_translator import VolumeSeries, Volume
from CCF_translator.deformation.route_calculation import find_hamiltonian_path, calculate_route
import copy


# Usage example
VOXEL_SIZE_MICRON = 20
SPACE_NAME = "demba_dev_mouse"
DATA_FOLDER = "/mnt/z/HBP_Atlasing/Developmental_atlases/DeMBA_Developmental mouse brain atlas/DeMBA-v1/01_working-environment/01_Data/DeMBA_v1/interpolated_templates/"
KEY_AGES = [7, 4]

volumes = []
for age in KEY_AGES:
    volume_path = os.path.join(DATA_FOLDER, f"DeMBA_P{age}_brain.nii.gz")
    try:
        volume_data = nib.load(volume_path).get_fdata()
    except FileNotFoundError:
        print(f"File not found: {volume_path}")
        continue
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