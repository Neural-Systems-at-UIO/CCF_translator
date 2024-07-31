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
        metadata_path = os.path.join(base_path, "metadata", "translation_metadata.csv")
        metadata = pd.read_csv(metadata_path)
        self.metadata = metadata

    def transform(self, target_age=None, target_space=None):
        array = self.values
        source = f"{self.space}_P{self.age_PND}"
        target = f"{target_space}_P{target_age}"
        route = route_calculation.calculate_route(source, target, self.metadata)
        deform_arr,pad_sum, array = apply_deformation.combine_route(route, array,base_path, self.metadata)
        if deform_arr is not None:                
            deform_arr = apply_deformation.resize_transformation(deform_arr, array.shape)
            order = 0 if self.segmentation_file else 1
            array = apply_deformation.apply_transform(array, deform_arr, order=order)
        else:
            array =apply_deformation.pad_neg(array, pad_sum, mode='constant')        
        self.values = array
        self.age_PND = target_age


# First we should try to calculate the route using all volumes
# Then we filter out the skippable ones
