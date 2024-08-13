"""I wanted to include the Gubra multimodal atlas but ran into a few issues. 
First the origin of the volumes is not zero so this had to be corrected for in the deformations.
Second, they transform between two volumes of different resolutions, something which I suspect may cause 
problems for CCF translator in the future, here is my attempt to correct for these issues. 
In the end it is close to the Gubra result, maybe off by less than 1 voxel. 
""" 

import nibabel as nib
import numpy as np
from scipy.ndimage import zoom

##set the origin as zero in the transform file if you want to use that with these files
##here we just remove the offsets from the volume that is to be registered
img = nib.load(f"Multimodal_mouse_brain_atlas_files/LSFM_space_oriented/lsfm_temp.nii.gz")
img.header['qoffset_x'] = 0
img.header['qoffset_y'] = 0
img.header['qoffset_z'] = 0
source_arr = np.asanyarray(img.dataobj)
img.affine[0,3] = 0
img.affine[1,3] = 0
img.affine[2,3] = 0
# out_im = nib.Nifti1Image(source_arr, img.affine, img.header)
# nib.save(out_im, f'lsfm_new_header.nii.gz')

##here we correct the deformation matrix so it has an origin of zero
img = nib.load("Multimodal_mouse_brain_atlas_files/Deformation_fields/lsfm_2_ccfv3_deffield.nii.gz")
target_shape = np.array(img.shape[:3])
diff = ((target_shape/2)- (np.array(source_arr.shape)/ 2)) 
arr = img.get_fdata()
###These numbers can be calculated as the midpoint of the source volume minus midpoint of target (maybe other way round)
arr[:,:,:,:,0] -= img.affine[0,0] * diff[0]
arr[:,:,:,:,1] -=  img.affine[1,1] * diff[1]
arr[:,:,:,:,2] -= img.affine[2,2] * diff[2]
arr = np.squeeze(arr,3)
arr = np.transpose(arr,(3,0,1,2))

zooms = [t/g for t,g in zip(arr.shape[1:], source_arr.shape )]
coords_orig_shape = np.mgrid[0:source_arr.shape[0], 0:source_arr.shape[1], 0:source_arr.shape[2]]


x = np.arange(0,coords_orig_shape.shape[1], coords_orig_shape.shape[1] / arr.shape[1])
y = np.arange(0,coords_orig_shape.shape[2], coords_orig_shape.shape[2] / arr.shape[2])
z = np.arange(0,coords_orig_shape.shape[3], coords_orig_shape.shape[3] / arr.shape[3])
X, Y, Z = np.meshgrid( x, y , z, indexing='ij')
coords_orig_resize = np.stack([X,Y,Z])




coords_target_shape = np.mgrid[0:arr.shape[1], 0:arr.shape[2], 0:arr.shape[3]]
coord_diff = coords_orig_resize - coords_target_shape 
###There seems to be less than a voxel of rounding error that I manually correct
coord_diff[0] -= 0.6
coord_diff[1] -= 0.1
coord_diff[2] -= 0.1
temp_arr = arr.copy()
final_arr = ((temp_arr  ) - coord_diff)
final_arr[0] *= zooms[0]
final_arr[1] *= zooms[1]
final_arr[2] *= zooms[2]
img.header['qoffset_x'] = 0
img.header['qoffset_y'] = 0
img.header['qoffset_z'] = 0
img.affine[0,-1] = 0
img.affine[1,-1] = 0
img.affine[2,-1] = 0
final_arr = np.transpose(final_arr,(1,2,3,0))
out_im = nib.Nifti1Image(final_arr[:,:,:,np.newaxis,:], img.affine, img.header)
nib.save(out_im, f'lsfm_2_ccfv3_zero_origin_same_size.nii.gz')


##set the origin as zero in the transform file if you want to use that with these files
##here we just remove the offsets from the volume that is to be registered
img = nib.load(f"Multimodal_mouse_brain_atlas_files/MRI_space_oriented/mri_temp.nii.gz")
img.header['qoffset_x'] = 0
img.header['qoffset_y'] = 0
img.header['qoffset_z'] = 0
source_arr = np.asanyarray(img.dataobj)
img.affine[0,3] = 0
img.affine[1,3] = 0
img.affine[2,3] = 0
out_im = nib.Nifti1Image(source_arr, img.affine, img.header)
nib.save(out_im, f'mri_new_header.nii.gz')

##here we correct the deformation matrix so it has an origin of zero
img = nib.load("Multimodal_mouse_brain_atlas_files/Deformation_fields/mri_2_ccfv3_deffield.nii.gz")
target_shape = np.array(img.shape[:3])
diff = ((target_shape/2)- (np.array(source_arr.shape)/ 2)) 
arr = img.get_fdata()
###These numbers can be calculated as the midpoint of the source volume minus midpoint of target (maybe other way round)
arr[:,:,:,:,0] -= img.affine[0,0] * diff[0]
arr[:,:,:,:,1] -=  img.affine[1,1] * diff[1]
arr[:,:,:,:,2] -= img.affine[2,2] * diff[2]
arr = np.squeeze(arr,3)
arr = np.transpose(arr,(3,0,1,2))

zooms = [t/g for t,g in zip(arr.shape[1:], source_arr.shape )]
coords_orig_shape = np.mgrid[0:source_arr.shape[0], 0:source_arr.shape[1], 0:source_arr.shape[2]]
coords_orig_resize = np.zeros(arr.shape)
for i in range(3):
    coords_orig_resize[i] = zoom(coords_orig_shape[i], zooms, order=0)
coords_target_shape = np.mgrid[0:arr.shape[1], 0:arr.shape[2], 0:arr.shape[3]]
coord_diff = coords_orig_resize - coords_target_shape 
#fudge factor
coord_diff[0] += 0.6
coord_diff[1] += 0.2
coord_diff[2] += 0.4
temp_arr = arr.copy()

final_arr = ((temp_arr  ) - coord_diff)
final_arr[0] *= zooms[0]
final_arr[1] *= zooms[1]
final_arr[2] *= zooms[2]

img.header['qoffset_x'] = 0
img.header['qoffset_y'] = 0
img.header['qoffset_z'] = 0
img.affine[0,-1] = 0
img.affine[1,-1] = 0
img.affine[2,-1] = 0
final_arr = np.transpose(final_arr,(1,2,3,0))
out_im = nib.Nifti1Image(final_arr[:,:,:,np.newaxis,:], img.affine, img.header)
nib.save(out_im, f'mri_2_ccfv3_zero_origin_same_size.nii.gz')






