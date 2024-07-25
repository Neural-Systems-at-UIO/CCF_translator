import numpy as np
from .deformation import apply_deformation, route_calculation 
import pandas as pd
import json
import os

base_path = os.path.dirname(__file__)

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
        source = '_'.join(self.space, self.age_PND)
        array = self.values
        direction = np.sign(target - source)
        key_age_df = self.metadata[self.metadata['key_age']]
        key_space_arr = key_age_df['source_space'].values

        if source not in key_space_arr:
            source_key = route_calculation.calculate_key_in_path(source, target, key_space_arr)
        else:
            source_key = source
        if target not in key_space_arr:
            target_key =  route_calculation.calculate_key_in_path(target, source, key_space_arr)
        else:
            target_key = target
        route = route_calculation.calculate_route(source_key,target_key,self.metadata[self.metadata['key_age']].to_dict('list'))
        route = [int(i.split('_P')[-1]) for i in route]
        if source not in key_space_arr:
            route.insert(0,source)
        if target not in key_space_arr:
            route.append(target)
        deform_arr = None
        for i in range(1,len(route)):
            start = route[i-1]
            stop  = route[i]
            magnitude = abs(stop-start)
            if stop not in key_space_arr:
                deform_path = os.path.join(base_path, "metadata", "deformation_fields", self.space, f"{stop}_pull_{stop - 1}.nii.gz")
                magnitude *= -1
            else:
                deform_path = os.path.join(base_path, "metadata", "deformation_fields", self.space,f"{stop}_pull_{stop - direction}.nii.gz")
            
            if deform_arr is None:
                deform_arr = apply_deformation.open_transformation(deform_path) * magnitude
            else:
                deform_b = apply_deformation.open_transformation(deform_path) * magnitude
                deform_arr = apply_deformation.combine_deformations(deform_arr,deform_b)
        translation_mag = key_age_df["transformation_resolution_micron"].iloc[0]
        if translation_mag != self.voxel_size_um:
            scale = translation_mag / self.voxel_size_um 
            deform_arr = apply_deformation.resize_transform(deform_arr, scale)
        order = 0 if self.segmentation_file else 1
        array = apply_deformation.apply_transform(array, deform_arr, order=order)
        self.values = array
        self.age_PND = target
