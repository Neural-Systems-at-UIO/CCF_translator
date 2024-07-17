import nibabel as nib
import scipy
import numpy as np
import h5py
import scipy.ndimage 
#import hdf5plugin


def open_transformation_nii(metadata_path):
    deformation_img = nib.load(metadata_path)
    deformation = np.asanyarray(deformation_img.dataobj)
    deformation =  np.transpose(deformation, (3,0,1,2))
    return deformation

def create_deformation_coords(deformation_arr):
    coords = np.mgrid[0:deformation_arr.shape[1], 0:deformation_arr.shape[2], 0:deformation_arr.shape[3]]
    deformed_coords = coords + deformation_arr
    return deformed_coords

def apply_transform(data, deformation, order=0):
    deformation_coords = create_deformation_coords(deformation)
    out_data = np.empty(data.shape)
    out_data = scipy.ndimage.map_coordinates(data, deformation_coords, order=order)
    return out_data



#create pnd28
deform_path = r"/home/harryc/github/DembaInterpolate2024/per_day_deformation/28_pull_29.nii.gz"
deform_arr = open_transformation_nii(deform_path)
#open P56 seg
seg_path = r"/home/harryc/github/CCF_translator/demo_data/DeMBA_P56_brain.nii.gz"
seg_img = nib.load(seg_path)
seg_arr = np.asanyarray(seg_img.dataobj)
#apply transformation
out_arr = apply_transform(seg_arr, deform_arr * (56-28))
#save output
out_img = nib.Nifti1Image(out_arr, seg_img.affine, header=seg_img.header)
nib.save(out_img, f"DeMBA_P{28}_test.nii.gz")

#create pnd56
deform_path = r"/home/harryc/github/DembaInterpolate2024/per_day_deformation/56_pull_55.nii.gz"
deform_arr = open_transformation_nii(deform_path)
#open P56 seg
seg_path =f"DeMBA_P{28}_test.nii.gz"
seg_img = nib.load(seg_path)
seg_arr = np.asanyarray(seg_img.dataobj)
#apply transformation
out_arr = apply_transform(seg_arr, deform_arr * (56-28))
#save output
out_img = nib.Nifti1Image(out_arr, seg_img.affine, header=seg_img.header)
nib.save(out_img, f"DeMBA_P{28}_test.nii.gz")


#create pnd42
deform_path = r"/home/harryc/github/DembaInterpolate2024/per_day_deformation/42_pull_41.nii.gz"
deform_arr = open_transformation_nii(deform_path)
#open P56 seg
seg_path = r"/home/harryc/github/CCF_translator/demo_data/DeMBA_P56_segmentation_2022.nii.gz"
seg_img = nib.load(seg_path)
seg_arr = np.asanyarray(seg_img.dataobj)
#apply transformation
out_arr = apply_transform(seg_arr, deform_arr * -(56-42))
#save output
out_img = nib.Nifti1Image(out_arr, seg_img.affine, header=seg_img.header)
nib.save(out_img, f"demo_data/DeMBA_P{42}_test.nii.gz")


#create pnd56
deform_path = r"/home/harryc/github/DembaInterpolate2024/per_day_deformation/56_pull_55.nii.gz"
deform_arr = open_transformation_nii(deform_path)
#open P56 seg
seg_path =  f"demo_data/DeMBA_P{42}_test.nii.gz"
seg_img = nib.load(seg_path)
seg_arr = np.asanyarray(seg_img.dataobj)
#apply transformation
out_arr = apply_transform(seg_arr, deform_arr * (56-42))
#save output
out_img = nib.Nifti1Image(out_arr, seg_img.affine, header=seg_img.header)
nib.save(out_img, f"demo_data/DeMBA_P{56}_test_2.nii.gz")

#create pnd42 10um resolution
deform_path = r"/home/harryc/github/DembaInterpolate2024/per_day_deformation/42_pull_41.nii.gz"
deform_arr = open_transformation_nii(deform_path)
#open P56 seg
seg_path = r"/home/harryc/github/CCF_translator/average_template_10_reoriented_padded.nii.gz"
seg_img = nib.load(seg_path)
seg_arr = np.asanyarray(seg_img.dataobj)
#apply transformation
def_shape = np.array(deform_arr.shape[1:])
arr_shape = np.array(seg_arr.shape)
if (arr_shape != def_shape).any():
    scale = [1]
    scale.extend(arr_shape/def_shape)
    deform_resize = scipy.ndimage.zoom(deform_arr, scale, order=0)
    deform_resize.shape





out_arr = apply_transform(seg_arr, deform_resize * -(56-42) * 2, order=1)
#save output
out_img = nib.Nifti1Image(out_arr, seg_img.affine, header=seg_img.header)
nib.save(out_img, f"demo_data/DeMBA_P{42}_test_10um_order_1.nii.gz")



#create pnd42 10um resolution
deform_path = r"/home/harryc/github/DembaInterpolate2024/per_day_deformation/42_pull_41.nii.gz"
deform_arr = open_transformation_nii(deform_path)
#open P56 seg
seg_path = r"/home/harryc/github/CCF_translator/demo_data/DeMBA_P56_brain.nii.gz"
seg_img = nib.load(seg_path)
seg_arr = np.asanyarray(seg_img.dataobj)
#apply transformation
def_shape = np.array(deform_arr.shape[1:])
arr_shape = np.array(seg_arr.shape)
out_arr = apply_transform(seg_arr, deform_arr * -(56-42))
#save output
out_img = nib.Nifti1Image(out_arr, seg_img.affine, header=seg_img.header)
nib.save(out_img, f"demo_data/DeMBA_P{42}_test_20um.nii.gz")

