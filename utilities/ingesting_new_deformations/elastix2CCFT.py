import nibabel as nib
import math
import pandas as pd
import numpy as np
from CCF_translator.deformation.forward_transform import invert_deformation
import os
root_path = r"/home/harryc/github/gubra/Multimodal_mouse_brain_atlas_files"
metadata = pd.read_csv(r"/home/harryc/github/CCF_translator/CCF_translator/metadata/translation_metadata.csv")
voxel_size_micron = 25

def open_deformation_field(deformation):
    """this function opens the elastix deformation
    and returns it in the format expected by CCF_translator"""
    deformation_arr = np.asanyarray(deformation.dataobj)
    def_header_dict = dict(deformation.header)
    x_sign = math.copysign(1,def_header_dict['qoffset_x'])
    y_sign = math.copysign(1,def_header_dict['qoffset_y'])
    z_sign = math.copysign(1,def_header_dict['qoffset_z'])
    dim_scale = 1/def_header_dict['pixdim'][1:4]
    dim_scale = np.array([x_sign,y_sign,z_sign]) * dim_scale
    deformation_arr_scaled = np.squeeze(deformation_arr,3)
    deformation_arr_scaled = np.transpose(deformation_arr_scaled,(3,0,1,2))
    dim_scale_reshaped = dim_scale.reshape(-1, 1, 1, 1)
    deformation_arr_scaled_multiplied = deformation_arr_scaled * dim_scale_reshaped
    return deformation_arr_scaled_multiplied

def save_volume(volume, file_name):
    affine = np.eye(4) 
    affine[:3,:3] *= voxel_size_micron
    volume = np.transpose(volume,(1,2,3,0))
    image = nib.Nifti1Image(volume, affine=affine)
    image.header.set_xyzt_units(3)
    nib.save(image, file_name)


source_spaces = ["gubra_mouse_mri", "gubra_mouse_lsfm"]
target_spaces = ["allen_mouse", "allen_mouse"]

original_elastix_volume_paths = [f'{root_path}/LSFM_space_oriented/lsfm_2_ccfv3_zero_origin.nii.gz',
                    f'{root_path}/MRI_space_oriented/mri_2_ccfv3_zero_origin.nii.gz']



for i in range(len(original_elastix_volume_paths)):
    original_elastix_volume_path = original_elastix_volume_paths[i]
    source = source_spaces[i]
    target = target_spaces[i]
    elastix_img = nib.load(original_elastix_volume_path)
    elastix_arr = open_deformation_field(elastix_img).astype(np.float32)
    save_path =  f"/home/harryc/github/CCF_translator/CCF_translator/metadata/deformation_fields/{source}/"
    if not os.path.isdir(save_path):
        os.mkdir(save_path)
    save_volume(elastix_arr,f"{save_path}/{target}_pull_{source}.nii.gz")
    inverted_arr = invert_deformation(elastix_arr)
    save_path =  f"/home/harryc/github/CCF_translator/CCF_translator/metadata/deformation_fields/{target}/"
    if not os.path.isdir(save_path):
        os.mkdir(save_path)
    save_volume(inverted_arr,f"{save_path}/{source}_pull_{target}.nii.gz")


metadata_template = {'file_name':[], 'source_space':[], 'target_space':[], 'affine':[], 'dim_order':[],
       'key_age':[], 'source_age_pnd':[], 'target_age_pnd':[], 'source_key_age':[],
       'target_key_age':[], 'padding_micron':[], 'transformation_resolution_micron':[],
       'X_physical_size_micron':[], 'Y_physical_size_micron':[],
       'Z_physical_size_micron':[], 'dim_flip':[], 'vector':[]}

for i in range(len(original_elastix_volume_paths)):
    original_elastix_volume_path = original_elastix_volume_paths[i]
    source = source_spaces[i]
    target = target_spaces[i]
    metadata_template['file_name'].append(f"{target}_pull_{source}.nii.gz")
    metadata_template['source_space'] = source
    metadata_template['target_space'] = target
    metadata_template['affine'].append(np.eye(4))
    metadata_template['dim_order'].append([0,1,2])
    metadata_template['key_age'].append(True)
    metadata_template['source_age_pnd'].append(56)
    metadata_template['target_age_pnd'].append(56)
    metadata_template['source_key_age'].append(False)
    metadata_template['target_key_age'].append(False)
    if target == "perens_stpt_mouse":
        metadata_template['X_physical_size_micron'].append(11400)
        metadata_template['Y_physical_size_micron'].append(16700)
        metadata_template['Z_physical_size_micron'].append(8000)
        metadata_template['transformation_resolution_micron'].append(25)
    if target == "perens_lsfm_mouse":
        metadata_template['X_physical_size_micron'].append(9225)
        metadata_template['Y_physical_size_micron'].append(12800)
        metadata_template['Z_physical_size_micron'].append(6700)
        metadata_template['transformation_resolution_micron'].append([25])
    if target == "perens_mri_mouse":
        metadata_template['X_physical_size_micron'].append(11375)
        metadata_template['Y_physical_size_micron'].append(15375)
        metadata_template['Z_physical_size_micron'].append(7425)
        metadata_template['transformation_resolution_micron'].append([25])


    metadata_template['dim_flip'].append([False,False,False])
    metadata_template['vector'].append(1)
    metadata_template['padding_micron'].append((0,0,0))

    metadata_template['file_name'].append(f"{source}_pull_{target}.nii.gz")
    metadata_template['source_space'] = target
    metadata_template['target_space'] = source
    metadata_template['affine'].append(np.eye(4))
    metadata_template['dim_order'].append([0,1,2])
    metadata_template['key_age'].append(True)
    metadata_template['source_age_pnd'].append(56)
    metadata_template['target_age_pnd'].append(56)
    metadata_template['source_key_age'].append(False)
    metadata_template['target_key_age'].append(False)
    metadata_template['X_physical_size_micron'].append(56)
    metadata_template['Y_physical_size_micron'].append(56)
    metadata_template['Z_physical_size_micron'].append(56)
    metadata_template['dim_flip'].append([False,False,False])
    metadata_template['vector'].append(1)
    metadata_template['padding_micron'].append((0,0,0))

pd.DataFrame(metadata_template)
metadata.to_csv(metadata_path)


