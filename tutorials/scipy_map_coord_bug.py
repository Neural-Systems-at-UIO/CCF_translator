from scipy import ndimage
import numpy as np

# Original array
a = np.arange(12).reshape((4, 3))
a[0, 0] = 99999999999999999
# Create deformation field
xy_deform = np.zeros((2,) + a.shape, dtype=np.float32)

# Apply a simple translation deformation: shift by 1 pixel down and to the right
y_deform, x_deform = np.meshgrid(np.arange(a.shape[0]), np.arange(a.shape[1]), indexing='ij')
xy_deform[0] = y_deform - 1  # shift down
xy_deform[1] = x_deform - 1  # shift right

# Apply deformation using map_coordinates
deformed_a = ndimage.map_coordinates(a, xy_deform, order=0) 




print(deformed_a)

