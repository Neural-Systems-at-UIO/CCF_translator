import numpy as np
import nibabel as nib
import scipy
from scipy.ndimage import map_coordinates


def create_deformation_coords(deformation_arr):
    coords = np.mgrid[0:deformation_arr.shape[1], 0:deformation_arr.shape[2], 0:deformation_arr.shape[3]]
    deformed_coords = coords + deformation_arr
    return deformed_coords

def open_transformation(transform_path):
    deformation_img = nib.load(transform_path)
    deformation = np.asarray(deformation_img.dataobj)
    deformation =  np.transpose(deformation, (3,0,1,2))
    return deformation

def apply_transform(data, deformation, order, apply_to_coords = False):
    deformation_coords = create_deformation_coords(deformation)
    out_data = np.empty(data.shape)
    if apply_to_coords:
        for i in range(data.shape[0]):
            out_data[i] = scipy.ndimage.map_coordinates(data[i], deformation_coords, order=order)
    else:
        out_data = scipy.ndimage.map_coordinates(data, deformation_coords, order=order)
    return out_data

def combine_deformations(deformation_a, deformation_b):
    deformation_a = apply_transform(deformation_a, deformation_b, order=1, apply_to_coords=True)
    return deformation_a + deformation_b

def resize_transform(arr, scale):
    """performs a regular grid interpolation"""
    # Original indices
    _, z_indices, y_indices, x_indices = np.indices(arr.shape)
    # New indices with double the resolution
    x_new_indices = np.linspace(x_indices.min(), x_indices.max(), arr.shape[3] * scale)
    y_new_indices = np.linspace(y_indices.min(), y_indices.max(), arr.shape[2] * scale)
    z_new_indices = np.linspace(z_indices.min(), z_indices.max(), arr.shape[1] * scale)
    # Create a grid of new indices
    new_indices = np.meshgrid(z_new_indices, y_new_indices, x_new_indices,  indexing='ij')
    new_shape = np.array(arr.shape) 
    new_shape[1:] *= scale
    new_array = np.zeros(new_shape)
    for i in range(3):
        # New array with double the resolution
        new_array[i] = map_coordinates(arr[i], new_indices, order=1)
    new_array = new_array*scale
    return new_array