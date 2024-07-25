import CCF_translator as CCFT
import nibabel as nib
import numpy as np
import json
import ast
import scipy
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from scipy.ndimage import map_coordinates

transform_base = rf"/home/harryc/github/CCF_translator/CCF_translator/metadata/deformation_fields/allen_mouse_CCF/"
metadata_path = r"/home/harryc/github/CCF_translator/CCF_translator/metadata/translation_volume_info.json"
with open(metadata_path, 'r') as f:
    metadata = pd.DataFrame(json.load(f))

source = 56
target = 20

seg_path = rf"/home/harryc/github/CCF_translator/demo_data/DeMBA_P{source}_segmentation_2022.nii.gz"
seg_img = nib.load(seg_path)
volume = np.array(seg_img.dataobj)

CCFT_vol = CCFT.volume(data=volume, 
                       space="CCFv3", 
                       voxel_size_um=20, 
                       age_PND=source, 
                       segmentation_file=True)

output_arr = transform_to_age(CCFT_vol, target, metadata)

img = nib.Nifti1Image(output_arr, seg_img.affine, header=seg_img.header)
nib.save(img, f"demo_data/DeMBA_P{target}_double.nii.gz")

source = 20
target = 56

seg_path = f"demo_data/DeMBA_P{source}_double.nii.gz"
seg_img = nib.load(seg_path)
seg_arr = np.array(seg_img.dataobj)
output_arr = transform_to_age(seg_arr, source, target, metadata)
img = nib.Nifti1Image(output_arr, seg_img.affine, header=seg_img.header)
nib.save(img, f"demo_data/DeMBA_P{target}_double.nii.gz")

"""10 micron example"""

source = 56
target = 20

seg_path = rf"/home/harryc/github/CCF_translator/demo_data/annotation_10_2022_reoriented_padded.nii.gz"
seg_img = nib.load(seg_path)
seg_arr = np.array(seg_img.dataobj)
output_arr = transform_to_age(seg_arr, source, target, metadata, scale=2)
img = nib.Nifti1Image(output_arr, seg_img.affine, header=seg_img.header)
nib.save(img, f"demo_data/DeMBA_P{target}_double.nii.gz")

deformation_a_path = f"{transform_base}/{28}_pull_{29}.nii.gz"
deformation_a = open_transformation(deformation_a_path)
deformation_a_2 = resize_transform(deformation_a,2)
arr = deformation_a

"""
deformation_a_path = f"{transform_base}/{28}_pull_{29}.nii.gz"
deformation_b_path = f"{transform_base}/{21}_pull_{22}.nii.gz"
deformation_a = open_transformation(deformation_a_path)
deformation_b = open_transformation(deformation_b_path)

##parallel
seg_img = nib.load(seg_path)
seg_arr = np.array(seg_img.dataobj)
deformation_ab = combine_deformations(deformation_a * 28, deformation_b * 7)
seg_arr = apply_transform(seg_arr, deformation_ab, order=0)
img = nib.Nifti1Image(seg_arr, seg_img.affine, header=seg_img.header)
nib.save(img, f"demo_data/DeMBA_P{21}_double.nii.gz")
#to 14
deformation_b_path = f"{transform_base}/{14}_pull_{15}.nii.gz"
deformation_b = open_transformation(deformation_b_path) * 7
deformation_ab = combine_deformations(deformation_ab, deformation_b)
seg_img = nib.load(seg_path)
seg_arr = np.array(seg_img.dataobj)
seg_arr = apply_transform(seg_arr, deformation_ab, order=0)
img = nib.Nifti1Image(seg_arr, seg_img.affine, header=seg_img.header)
nib.save(img, f"demo_data/DeMBA_P{14}_double.nii.gz")
#to 7
deformation_b_path = f"{transform_base}/{7}_pull_{8}.nii.gz"
deformation_b = open_transformation(deformation_b_path) * 7
deformation_ab = combine_deformations(deformation_ab, deformation_b)
seg_img = nib.load(seg_path)
seg_arr = np.array(seg_img.dataobj)
seg_arr = apply_transform(seg_arr, deformation_ab, order=0)
img = nib.Nifti1Image(seg_arr, seg_img.affine, header=seg_img.header)
nib.save(img, f"demo_data/DeMBA_P{7}_double.nii.gz")
#to 4
deformation_b_path = f"{transform_base}/{4}_pull_{5}.nii.gz"
deformation_b = open_transformation(deformation_b_path) * 3
deformation_ab = combine_deformations(deformation_ab, deformation_b)
seg_img = nib.load(seg_path)
seg_arr = np.array(seg_img.dataobj)
seg_arr = apply_transform(seg_arr, deformation_ab, order=0)
img = nib.Nifti1Image(seg_arr, seg_img.affine, header=seg_img.header)
nib.save(img, f"demo_data/DeMBA_P{4}_double.nii.gz")
"""