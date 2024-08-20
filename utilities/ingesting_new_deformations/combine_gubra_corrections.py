###Jobs for tomorrow
###Interpolate missing values so that the arrays are complete
###Invert transforms on big computer
###Calculate transform from oriented to orig
###Finalise metadata


from scipy.ndimage import map_coordinates
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
from scipy.ndimage import zoom
import scipy
import json
import os
from scipy.ndimage import map_coordinates
import requests


root_path = r"/home/harryc/github/gubra/Multimodal_mouse_brain_atlas_files"
out_path = r"/home/harryc/github/CCF_translator/CCF_translator/"

def create_deformation_coords(deformation_arr):
    coords = np.mgrid[0:deformation_arr.shape[1], 0:deformation_arr.shape[2], 0:deformation_arr.shape[3]]
    deformed_coords = coords + deformation_arr
    return deformed_coords

def open_transformation(transform_path):        
    deformation_img = nib.load(transform_path)
    deformation = np.asarray(deformation_img.dataobj)
    deformation =  np.transpose(deformation, (3,0,1,2))
    return deformation


def combine_deformations(deformation_a, deformation_b):
    deformation_a = apply_transform(deformation_a, deformation_b, order=2, apply_to_coords=True)
    return deformation_a + deformation_b


def apply_transform(data, deformation, order, apply_to_coords = False):
    deformation_coords = create_deformation_coords(deformation)
    if apply_to_coords:
        out_data = np.empty(deformation.shape)
        for i in range(data.shape[0]):
            out_data[i] = scipy.ndimage.map_coordinates(data[i], deformation_coords, order=order)
    else:
        out_data = np.empty(deformation[0].shape)
        out_data = scipy.ndimage.map_coordinates(data, deformation_coords, order=order)
    return out_data

def resize_transform(arr, scale):
    """performs a regular grid interpolation"""
    # Original indices
    _, z_indices, y_indices, x_indices = np.indices(arr.shape)
    # New indices with double the resolution
    x_new_indices = np.linspace(x_indices.min(), x_indices.max(),   int(arr.shape[3] * scale[3]))
    y_new_indices = np.linspace(y_indices.min(), y_indices.max(),   int(arr.shape[2] * scale[2]))
    z_new_indices = np.linspace(z_indices.min(), z_indices.max(),   int(arr.shape[1] * scale[1]))

    # Create a grid of new indices
    new_indices = np.meshgrid(z_new_indices, y_new_indices, x_new_indices,  indexing='ij')
    new_shape = np.array(arr.shape) 
    new_shape[1] = new_shape[1] * scale[1]
    new_shape[2] = new_shape[2] * scale[2]
    new_shape[3] = new_shape[3] * scale[3]
    new_array = np.zeros(new_shape)
    for i in range(3):
        # New array with double the resolution
        new_array[i] = map_coordinates(arr[i], new_indices, order=1)
    new_array[0] = new_array[0]*scale[1]
    new_array[1] = new_array[1]*scale[2]
    new_array[2] = new_array[2]*scale[3]
    return new_array


def calculate_offset(original_input_shape, output_shape):
    x = np.arange(0,original_input_shape[1], original_input_shape[1] / output_shape[1])
    y = np.arange(0,original_input_shape[2], original_input_shape[2] / output_shape[2])
    z = np.arange(0,original_input_shape[3], original_input_shape[3] / output_shape[3])
    X, Y, Z = np.meshgrid(x,y,z, indexing='ij')
    original_coordinates = np.stack([X,Y,Z])
    target_coordinates = np.indices(output_shape[1:])
    coordinate_difference =  original_coordinates - target_coordinates 
    return coordinate_difference    

def resize_input(arr, original_input_shape, new_input_shape):
    out_arr = arr.copy()
    """This function changes the input size of a transformation without changing the output"""
    output_shape = out_arr.shape
    initial_offset = calculate_offset(original_input_shape, output_shape)
    out_arr -= initial_offset
    scale = np.array(new_input_shape) / np.array(original_input_shape)
    out_arr[0] *= scale[1]
    out_arr[1] *= scale[2]
    out_arr[2] *= scale[3]
    new_offset = calculate_offset(new_input_shape, output_shape)
    out_arr += new_offset
    return out_arr

perens_stpt = nib.load(f'{root_path}/AIBS_CCFv3_space_oriented/ccfv3_new_header.nii.gz')
perens_stpt_arr = perens_stpt.get_fdata()
save_path = r"/home/harryc/github/CCF_translator/CCF_translator/metadata/deformation_fields/perens_stpt_mouse"
first = nib.load(f"{save_path}/perens_mri_mouse_pull_perens_stpt_mouse.nii.gz")
##here we correct the deformation matrix so it has an origin of zero
first_arr = first.get_fdata()
first_arr =  np.transpose(first_arr, (3,0,1,2))
save_path = r"/home/harryc/github/CCF_translator/CCF_translator/metadata/deformation_fields/perens_mri_mouse"
second = nib.load( f"{save_path}/allen_mouse_pull_perens_mri_mouse.nii.gz")
second_arr = second.get_fdata()
second_arr =  np.transpose(second_arr, (3,0,1,2))
save_path = r"/home/harryc/github/CCF_translator/CCF_translator/metadata/deformation_fields/allen_mouse"
###The first arr must have the same input size as the second when adding together
first_arr_output_size = np.array(first_arr.shape[1:])
second_arr_output_size = np.array(second_arr.shape[1:])
first_arr = resize_input(first_arr, (1,*perens_stpt_arr.shape),  (1,*first_arr.shape[1:]))
ccf2orig = combine_deformations(first_arr, second_arr)
ccf2orig = resize_input(ccf2orig, (1,*first_arr.shape[1:]), (1,*perens_stpt_arr.shape))
test_transform = apply_transform(perens_stpt_arr, ccf2orig, order=1)
transform_out = nib.Nifti1Image(ccf2orig, np.eye(4))
nib.save(transform_out, f"/home/harryc/github/CCF_translator/CCF_translator/metadata/deformation_fields/perens_stpt_mouse/allen_mouse_pull_perens_stpt_mouse.nii.gz")
test_out = nib.Nifti1Image(test_transform, perens_stpt.affine, perens_stpt.header)
nib.save(test_out,f"stpt_warped_2_stpt.nii.gz" )
