import numpy as np
import nibabel as nib
import scipy
import json
import os
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

def resize_transformation(deform_arr, array_size):
    if (np.array(deform_arr.shape)[1:] != np.array(array_size)).all():
        scale = (1, *(np.array(array_size) / np.array(deform_arr.shape)[1:]))
        deform_arr = resize_transform(deform_arr, scale)
    return deform_arr

def pad_neg(array, padding, mode):
    padding = np.round(padding).astype(int)
    for i in range(len(padding)):
        if padding[i][0] < 0:
            array = np.delete(array, np.s_[:abs(padding[i][0])], axis=i)
            padding[i][0] = 0
        if padding[i][1] < 0:
            array = np.delete(array, np.s_[-abs(padding[i][1]):], axis=i)
            padding[i][1] = 0
    array = np.pad(array, padding, mode=mode)
    return array

def combine_route(route, array,base_path, metadata):
    deform_arr = None
    pad_sum = np.zeros((3,2))
    source_metadata = (
        metadata["source_space"] + "_P" + metadata["source_age_pnd"].astype(str)
    )
    target_metadata = (
        metadata["target_space"] + "_P" + metadata["target_age_pnd"].astype(str)
    )
    for i in range(1, len(route)):
        start = route[i - 1]
        stop = route[i]
        translation_metadata = metadata[
            (source_metadata == stop) & (target_metadata == start)
        ]
        if len(translation_metadata) > 1:
            raise Exception("Error more than one matching transformation found.")
        translation_metadata = translation_metadata.to_dict(orient="list")

        if translation_metadata['padding_micron'] != "[[0, 0], [0, 0], [0, 0]]":
            padding = np.array(json.loads(translation_metadata['padding_micron'][0]))
            X_physical_size_micron = translation_metadata['X_physical_size_micron']
            Y_physical_size_micron = translation_metadata['Y_physical_size_micron']
            Z_physical_size_micron = translation_metadata['Z_physical_size_micron']
            x_pad = (padding[0] / X_physical_size_micron) * array.shape[0]
            y_pad = (padding[1] / Y_physical_size_micron) * array.shape[1]
            z_pad = (padding[2] / Z_physical_size_micron) * array.shape[2]
            temp_padding = np.array([x_pad, y_pad, z_pad])
            pad_sum+=temp_padding
            #array = pad_neg(array, temp_padding, mode='constant')
            if deform_arr is not None:
                for i in range(3):
                    deform_arr[i] -= temp_padding[i][0]
                    deform_arr[i] += temp_padding[i][1]
                deform_padding = np.concatenate(([[0, 0]], temp_padding), axis=0)
                deform_arr  = pad_neg(deform_arr, deform_padding, mode='constant')
        if translation_metadata['dim_order'][0] != '[0, 1, 2]':
            dim_order = list(map(int, translation_metadata['dim_order'][0][1:-1].split(', ')))
            array = np.transpose(array, dim_order)
            pad_sum = pad_sum[dim_order]
            if deform_arr is not None:
                deform_dim = np.array(dim_order.copy())
                deform_dim = deform_dim + 1
                deform_dim = [0, *deform_dim]
                deform_arr  = np.transpose(deform_arr, deform_dim)
                deform_arr = deform_arr[dim_order]
        if translation_metadata['dim_flip'][0] != '[False, False, False]':
            dim_flip = list(map(eval, translation_metadata['dim_flip'][0][1:-1].split(', ')))
            for i in range(3):
                if dim_flip[i]:
                    pad_sum[i] = pad_sum[i][::-1]
                    array = np.flip(array, axis=i)
                    if deform_arr is not None:
                        deform_arr  = np.flip(deform_arr, axis=i+1)
                        deform_arr[i] *= -1
                        

        if translation_metadata["file_name"][0]!='False':
            vector = translation_metadata["vector"][0]
            vector = int(vector)
            deform_path = deform_path = os.path.join(
                base_path,
                "metadata",
                "deformation_fields",
                translation_metadata["source_space"][0],
                translation_metadata["file_name"][0],
            )
            if deform_arr is None:
                deform_arr = open_transformation(deform_path) * vector
            else:
                deform_b = open_transformation(deform_path) * vector
                if (np.array(deform_b.shape) != np.array(deform_arr.shape)).all():
                    deform_b = resize_transformation(deform_b, deform_arr.shape)
                deform_arr = combine_deformations(deform_arr, deform_b)
    return deform_arr,pad_sum, array

