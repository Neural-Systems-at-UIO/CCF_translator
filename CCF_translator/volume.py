import numpy as np
from .deformation import apply_deformation, route_calculation 
import pandas as pd
import json
import os

base_path = os.path.dirname(__file__)



def calculate_keys(source, target, key_age_arr):
    if source not in key_age_arr:
        source_key = route_calculation.calculate_key_in_path(source, target, key_age_arr)
    else:
        source_key = source
    if target not in key_age_arr:
        target_key = route_calculation.calculate_key_in_path(target, source, key_age_arr)
    else:
        target_key = target
    return source_key, target_key

def calculate_route(space, source_key, target_key, key_age_arr):
    route = route_calculation.calculate_route(f'{space}_P{source_key}', f'{space}_P{target_key}', self.metadata[self.metadata['key_age']].to_dict('list'))
    route = [int(i.split('_P')[-1]) for i in route]
    if source_key not in key_age_arr:
        route.insert(0, source_key)
    if target_key not in key_age_arr:
        route.append(target_key)
    return route

def generate_deformation_path(stop, key_age_arr, space, direction):
    if stop not in key_age_arr:
        deform_path = os.path.join(base_path, "metadata", "deformation_fields", space, f"{stop}_pull_{stop - 1}.nii.gz")
    else:
        deform_path = os.path.join(base_path, "metadata", "deformation_fields", space, f"{stop}_pull_{stop - direction}.nii.gz")
    return deform_path

def apply_deformations(route, key_age_arr, direction):
    deform_arr = None
    for i in range(1, len(route)):
        start = route[i - 1]
        stop = route[i]
        magnitude = abs(stop - start)
        if stop not in key_age_arr:
            magnitude *= -1
        deform_path = generate_deformation_path(stop, direction)
        if deform_arr is None:
            deform_arr = apply_deformation.open_transformation(deform_path) * magnitude
        else:
            deform_b = apply_deformation.open_transformation(deform_path) * magnitude
            deform_arr = apply_deformation.combine_deformations(deform_arr, deform_b)
    return deform_arr

def resize_transformation(deform_arr, key_age_df, voxel_size_um):
    translation_mag = key_age_df["transformation_resolution_micron"].iloc[0]
    if translation_mag != voxel_size_um:
        scale = translation_mag / voxel_size_um
        deform_arr = apply_deformation.resize_transform(deform_arr, scale)
    return deform_arr

class volume:
    def __init__(self, values, space, voxel_size_um, age_PND, segmentation_file=False):
        self.values = values
        self.space = space
        self.voxel_size_um = voxel_size_um
        self.age_PND = age_PND
        self.segmentation_file = segmentation_file
        metadata_path = os.path.join(base_path,"metadata","translation_volume_info.json")
        with open(metadata_path, 'r') as f:
            metadata = pd.DataFrame(json.load(f))
        self.metadata = metadata
        pass

    def transform_to_age(self, target):
        source = self.age_PND
        array = self.values
        direction = np.sign(target - source)
        key_age_df = self.metadata[self.metadata['key_age']]
        key_age_arr = key_age_df['source_age_pnd'].values
        source_key, target_key = calculate_keys(source, target, key_age_arr)
        route = calculate_route(self.space, source_key, target_key, key_age_arr)
        deform_arr = apply_deformations(route, key_age_arr, direction)


        deform_arr = resize_transformation()
        order = 0 if self.segmentation_file else 1
        array = apply_deformation.apply_transform(array, deform_arr, order=order)
        self.values = array
        self.age_PND = target
