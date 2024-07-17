from transformation_functions import forward_transform
import nibabel as nib
import numpy as np
import math
import scipy

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

def create_deformation_coords(deformation_arr):
    coords = np.mgrid[0:deformation_arr.shape[1], 0:deformation_arr.shape[2], 0:deformation_arr.shape[3]]
    deformed_coords = coords + deformation_arr
    return deformed_coords

def apply_transform(data, deformation, order=0):
    deformation_coords = create_deformation_coords(deformation)
    out_data = np.empty(data.shape)
    out_data = scipy.ndimage.map_coordinates(data, deformation_coords, order=order)
    return out_data

#The transformation volume is in the shape of P28 and pulls values from 56
transformation_path = r"deformations_from_elastix/P56_to_P28.nii.gz"
transformation_img = nib.load(transformation_path)
transformation_vol = open_elastix_deformation_field(transformation_img)

#normalise the transformation to just one day
#Now it is in P28 and pulling from P29
days = 56 - 28
transformation_vol = transformation_vol / days
#By applying it to itself it is now it is in P29 and pulling from P30 
P29_Pull_P30 = forward_transform(transformation_vol, -transformation_vol)

#Since its a linear transform pushing to 54 from 55 is the same as pulling 56 from 55
seg_path = r"/home/harryc/github/CCF_translator/demo_data/DeMBA_P56_segmentation_2022.nii.gz"
seg_img = nib.load(seg_path)
seg_arr = np.array(seg_img.dataobj)
P55_seg_arr = apply_transform(seg_arr, P29_Pull_P30 * 27)

img = nib.Nifti1Image(P55_seg_arr, seg_img.affine, header=seg_img.header)
nib.save(img, f"DeMBA_P{29}_seg_test.nii.gz")








#If we would like to transform 28 to 55 all we need to do is multiply this by -1 and 27


#Since its a linear transform pushing to 54 from 55 is the same as pulling 56 from 55
seg_path = r"/home/harryc/github/CCF_translator/demo_data/DeMBA_P56_segmentation_2022.nii.gz"
seg_img = nib.load(seg_path)
seg_arr = np.array(seg_img.dataobj)
P55_seg_arr = apply_transform(seg_arr, transformation_vol) #P55_Push_P54 * -1 * 27)

img = nib.Nifti1Image(P55_seg_arr, seg_img.affine, header=seg_img.header)
nib.save(img, f"DeMBA_P{28}_seg_test_4.nii.gz")


"""Things I am pretty sure about
1. That apply transform needs values in the target space specifying where to pull them from in the source space
2. That applying apply transform straight to the deformation matrix from elastix makes a P28 vol from a P56 one
3. So... unless I have made a mistake, the output of elastix is in P28 space and is pulling in values from P56
"""