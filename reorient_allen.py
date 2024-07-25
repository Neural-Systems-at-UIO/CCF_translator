import nrrd
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import scipy.ndimage


path = r"/home/harryc/github/CCF_translator/demo_data/average_template_10.nrrd"
target_header = r"/home/harryc/github/CCF_translator/demo_data/average_template_10_reoriented_padded.nii.gz"
target = nib.load(target_header)
target_arr = np.asanyarray(target.dataobj)
target_shape = target.shape

anno_orig, header = nrrd.read(path)
anno = np.pad(anno_orig, [[0,90],[0,0],[0,0]])



anno = np.transpose(anno_orig, (2,1,0))
#out_im = nib.Nifti1Image(anno, target.affine, target.header)
#nib.save(out_im,  r"/home/harryc/github/CCF_translator/demo_data/average_template_10_reoriented.nii.gz")
#anno.shape
#zoom_factor = np.divide( target.shape, anno.shape)
#anno_resize = ndimage.zoom(anno, zoom_factor)


#out_im = nib.Nifti1Image(anno_resize, target.affine, target.header)
#nib.save(out_im,  r"/home/harryc/github/CCF_translator/demo_data/average_template_10_reoriented_rescaled.nii.gz")
path = r"/home/harryc/github/CCF_translator/demo_data/average_template_10_reoriented_rescaled.nii.gz"
ann_ = nib.load(path)
anno = np.asanyarray(ann_.dataobj)
# # resize with zoom



1320 * 10

(90 * (1410/1320)) * (1320/1410)


affine_matrix = np.array([[0, 0, 1, 0],
                          [0, 1, 0, 0],
                          [1, 0, 0, 0],
                          [0, 0, 0, 1]])

affine = np.eye(4)
affine[2,2] =  1320 / 1410  
#affine[2,3] = -45
print(anno.shape)
anno = scipy.ndimage.affine_transform(anno, np.linalg.inv(affine_matrix))
print(anno.shape)
#pad = ((0,0),(0,0),(0,90))
#anno = np.pad(anno, pad)
plt.imshow(target_arr[300] )
plt.show()
plt.imshow((anno[300]).astype(float) - (target_arr[300] ).astype(float))
plt.show()

#Data should be maintained as much as påossible



# Create a grid of coordinates in the original image
coordinates = np.indices(anno.shape)

# Add a row of ones to the coordinates to make them homogeneous
ones = np.ones((1,) + coordinates.shape[1:])
coordinates = np.vstack((coordinates, ones))

# Apply the affine transformation to the coordinates
transformed_coordinates = np.linalg.inv(affine).dot(coordinates.reshape(4, -1))

# Reshape the coordinates to their original shape
transformed_coordinates = transformed_coordinates[:3].reshape(-1, *anno.shape)

# Map the input image to the transformed coordinates
transformed_volume = scipy.ndimage.map_coordinates(anno, transformed_coordinates, order=1)
plt.imshow((transformed_volume[300]).astype(float) - (target_arr[300] ).astype(float))
plt.show()


#If the volume takes up a different amount of 

out_im = nib.Nifti1Image(transformed_volume, target.affine, target.header)
nib.save(out_im,  r"/home/harryc/github/CCF_translator/demo_data/transformed_volume.nii.gz")