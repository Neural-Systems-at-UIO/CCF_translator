import numpy as np
from .deformation import apply_deformation, route_calculation
import pandas as pd
import json
import os

base_path = os.path.dirname(__file__)


def calculate_keys(source, target, key_age_arr):
    if source not in key_age_arr:
        source_key = route_calculation.calculate_key_in_path(
            source, target, key_age_arr
        )
    else:
        source_key = source
    if target not in key_age_arr:
        target_key = route_calculation.calculate_key_in_path(
            target, source, key_age_arr
        )
    else:
        target_key = target
    return source_key, target_key
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

def combine_route(route, array, metadata):
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
                deform_arr = apply_deformation.open_transformation(deform_path) * vector
            else:
                deform_b = apply_deformation.open_transformation(deform_path) * vector
                deform_arr = apply_deformation.combine_deformations(deform_arr, deform_b)
    return deform_arr,pad_sum, array


def resize_transformation(deform_arr, array_size):
    if (np.array(deform_arr.shape)[1:] != np.array(array_size)).all():
        scale = (1, *(np.array(array_size) / np.array(deform_arr.shape)[1:]))
        deform_arr = apply_deformation.resize_transform(deform_arr, scale)
    return deform_arr


class volume:
    def __init__(self, values, space, voxel_size_um, age_PND, segmentation_file=False):
        self.values = values
        self.space = space
        self.voxel_size_um = voxel_size_um
        self.age_PND = age_PND
        self.segmentation_file = segmentation_file
        metadata_path = os.path.join(base_path, "metadata", "translation_metadata.csv")
        metadata = pd.read_csv(metadata_path)
        self.metadata = metadata

    def transform(self, target_age=None, target_space=None):
        array = self.values
        source = f"{self.space}_P{self.age_PND}"
        target = f"{target_space}_P{target_age}"
        route = route_calculation.calculate_route(source, target, self.metadata)

        deform_arr,pad_sum, array = combine_route(route, array, self.metadata)
        if deform_arr is not None:                
            deform_arr = resize_transformation(deform_arr, array.shape)
            order = 0 if self.segmentation_file else 1
            array = apply_deformation.apply_transform(array, deform_arr, order=order)
        else:
            array = pad_neg(array, pad_sum, mode='constant')        
        self.values = array
        self.age_PND = target_age


# First we should try to calculate the route using all volumes
# Then we filter out the skippable ones
