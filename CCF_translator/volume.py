import numpy as np
from .deformation import apply_deformation, route_calculation
import pandas as pd
import json
import os
import nibabel as nib

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
        deform_arr, pad_sum, array = apply_deformation.combine_route(
            route, array, base_path, self.metadata
        )
        if deform_arr is not None:
            new_shape = np.array(array.shape) + pad_sum[:,0] + pad_sum[:,1]
            deform_arr = apply_deformation.resize_transformation(
                deform_arr, new_shape
            )
            order = 0 if self.segmentation_file else 1
            array = apply_deformation.apply_transform(array, deform_arr, order=order)

        self.values = array
        self.age_PND = target_age

    def save(self, save_path):
        vol_metadata = {
            "space": self.space,
            "age_PND": self.age_PND,
            "segmentation_file": self.segmentation_file,
        }
        affine = np.eye(4)
        affine[:3, :3] *= self.voxel_size_um
        image = nib.Nifti1Image(self.values, affine=affine)
        image.header["descrip"] = vol_metadata
        image.header.set_xyzt_units(3)
        nib.save(image, save_path)


# First we should try to calculate the route using all volumes
# Then we filter out the skippable ones
