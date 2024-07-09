from transformation_functions import forward_transform
import nibabel as nib
import numpy as np
import math


def open_elastix_deformation_field(deformation):
    deformation_arr = np.asarray(deformation.dataobj)
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


#The transformation volume is in the shape of P28 and pulls in values from 56
transformation_path = r"deformations_from_elastix/P56_to_P28.nii.gz"
transformation_img = nib.load(transformation_path)
transformation_vol = open_elastix_deformation_field(transformation_img)

#normalise the transformation to just one day
days = 56 - 28
transformation_vol = transformation_vol / days



P29_P30 = forward_transform(transformation_vol, -transformation_vol)
