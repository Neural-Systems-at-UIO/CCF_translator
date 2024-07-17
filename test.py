import nibabel as nib
import scipy
import numpy as np
import h5py 
#import hdf5plugin


def open_transformation_nii(metadata_path):
    deformation_img = nib.load(metadata_path)
    deformation = deformation_img.get_fdata()
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

#def manual_forward_transform(data, deform):
    

"""Simple Case of 56 to 28"""
#open segmentation
age = 28
target = 56
seg_path = rf"/home/harryc/github/CCF_translator/demo_data/DeMBA_P{age}_segmentation_2022.nii.gz"
seg_img = nib.load(seg_path)
seg_arr = np.array(seg_img.dataobj)
#open deformation 
transform_path = r"/home/harryc/github/CCF_translator/CCF_translator/metadata/deformation_fields/allen_mouse_CCF/P28_to_P56.nii.gz"

deformation = open_transformation_nii(transform_path) 
#transform volume
out_file = apply_transform(seg_arr, deformation)

img = nib.Nifti1Image(out_file, seg_img.affine, header=seg_img.header)
nib.save(img, f"DeMBA_P{target}_simple_repro_rev.nii.gz")


"""Less simple case of 41 to 28"""
seg_path = r"/home/harryc/github/CCF_translator/demo_data/DeMBA_P41_segmentation_2022.nii.gz"
seg_img = nib.load(seg_path)
seg_arr = np.array(seg_img.dataobj)
transform_path = r"/home/harryc/github/CCF_translator/CCF_translator/metadata/deformation_fields/allen_mouse_CCF/P56_to_P28.nii.gz"
deformation = (open_transformation_nii(transform_path) / 28).astype(np.float32)
gap = 56-41
out_def = np.zeros_like(deformation)
for i in range(3):
    out_def[i] = apply_transform(deformation[i].copy(), (deformation * gap).astype(np.float32), order=1).astype(np.float32)
del deformation
out_file = apply_transform(seg_arr, out_def * 13)
img = nib.Nifti1Image(out_file, seg_img.affine, header=seg_img.header)
nib.save(img, f"demo_data/DeMBA_P{28}_simple_repro_from_41_order2.nii.gz")
