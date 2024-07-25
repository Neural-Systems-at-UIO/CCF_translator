import nrrd
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import scipy.ndimage
def affine_pad(axis, pad_size):
    # Create an identity matrix
    affine = np.eye(4)

    # Pad the specified axis
    affine[axis, -1] = pad_size

    return affine

path = r"/home/harryc/github/CCF_translator/demo_data/average_template_10_reoriented_rescaled.nii.gz"
target_header = r"/home/harryc/github/CCF_translator/demo_data/average_template_10_reoriented_padded.nii.gz"
target = nib.load(target_header)
target_arr = np.asanyarray(target.dataobj)
# anno_orig, header = nrrd.read(path)

anno = np.transpose(anno_orig, (2,1,0))
out_im = nib.Nifti1Image(anno, target.affine, target.header)
nib.save(out_im,  r"/home/harryc/github/CCF_translator/demo_data/average_template_10_reoriented.nii.gz")
anno.shape
target_shape = target.shape
#zoom_factor = np.divide( target.shape, anno.shape)
#anno_resize = ndimage.zoom(anno, zoom_factor)


#out_im = nib.Nifti1Image(anno_resize, target.affine, target.header)
#nib.save(out_im,  r"/home/harryc/github/CCF_translator/demo_data/average_template_10_reoriented_rescaled.nii.gz")

ann_ = nib.load(path)
anno = np.asanyarray(ann_.dataobj)
# resize with zoom

affine = np.eye(4)
affine[2,2] =  1320 / 1410  
#affine[2,3] = -45
print(anno.shape)
anno = scipy.ndimage.affine_transform(anno, np.linalg.inv(affine), output_shape=(1140, 800, 1410))
print(anno.shape)
#pad = ((0,0),(0,0),(0,90))
#anno = np.pad(anno, pad)
plt.imshow(target_arr[300] > 0)
plt.show()
plt.imshow((anno[300]).astype(float) - (target_arr[300] ).astype(float))
plt.show()



(anno == target_arr).all()


anno = 



out_im = nib.Nifti1Image(anno, target.affine, target.header)
nib.save(out_im,  r"/home/harryc/github/CCF_translator/demo_data/annotation_10_reoriented_padded_via_affine.nii.gz")

anno.shape

import numpy as np
import scipy.ndimage

def affine_pad(axis, pad_size):
    # Create an identity matrix
    affine = np.eye(4)

    # Pad the specified axis
    affine[axis, -1] = pad_size

    return affine

# Define a volume
volume = np.random.rand(10, 10, 10)

# Define an affine transformation
#affine = affine_pad(0, 5)  # Pad the x-axis by 5 units

# Create a grid of coordinates in the original image
coordinates = np.indices(volume.shape)

# Add a row of ones to the coordinates to make them homogeneous
coordinates = np.vstack((coordinates, np.ones(coordinates.shape[1:])))

# Apply the affine transformation to the coordinates
transformed_coordinates = np.linalg.inv(affine).dot(coordinates.reshape(4, -1))

# Reshape the coordinates to their original shape
transformed_coordinates = transformed_coordinates[:3].reshape(-1, *volume.shape)

# Map the input image to the transformed coordinates
transformed_volume = scipy.ndimage.map_coordinates(volume, transformed_coordinates, order=1)

print(transformed_volume)

#If the volume takes up a different amount of 