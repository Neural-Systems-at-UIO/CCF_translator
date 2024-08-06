import numpy as np
from .deformation import apply_deformation, route_calculation
import pandas as pd
import json
import os
import nibabel as nib

base_path = os.path.dirname(__file__)


class volume:
    def __init__(self, values, space, voxel_size_micron, age_PND, segmentation_file=False):
        self.values = values
        self.space = space
        self.voxel_size_micron = voxel_size_micron
        self.age_PND = age_PND
        self.segmentation_file = segmentation_file
        metadata_path = os.path.join(base_path, "metadata", "translation_metadata.csv")
        metadata = pd.read_csv(metadata_path)
        self.metadata = metadata

    def transform(self, target_age, target_space):
        array = self.values
        source = f"{self.space}_P{self.age_PND}"
        target = f"{target_space}_P{target_age}"
        if source == target:
            print("volume is already in that space")
            return
        route = route_calculation.calculate_route(source, target, self.metadata)
        deform_arr, pad_sum, flip_sum, dim_order_sum = apply_deformation.combine_route(
            route, array.shape, base_path, self.metadata
        )
        array = np.transpose(array, dim_order_sum)
        for i in range(len(flip_sum)):
            if flip_sum[i]:
                array = np.flip(array, axis=i)
        if deform_arr is not None:
            new_shape = np.array(array.shape) + pad_sum[:,0] + pad_sum[:,1]
            deform_arr = apply_deformation.resize_transformation(
                deform_arr, new_shape
            )
            order = 0 if self.segmentation_file else 1
            array = apply_deformation.apply_transform(array, deform_arr, order=order)
        else:
            array = apply_deformation.pad_neg(array, pad_sum, mode='constant')
        self.values = array
        self.age_PND = target_age
        self.space = target_space

    def save(self, save_path):
        vol_metadata = {
            "space": self.space,
            "age_PND": self.age_PND,
            "segmentation_file": self.segmentation_file,
        }
        affine = np.eye(4)
        affine[:3, :3] *= self.voxel_size_micron
        image = nib.Nifti1Image(self.values, affine=affine)
        image.header["descrip"] = vol_metadata
        image.header.set_xyzt_units(3)
        nib.save(image, save_path)


