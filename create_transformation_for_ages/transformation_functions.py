import numpy as np
from KNearestNDInterpolator import NearestNDInterpolator
from scipy.ndimage import binary_dilation, binary_erosion

def interpolate_array(arr):
    # Get the indices of the elements that are not NaN
    not_nan = np.logical_not(np.isnan(arr))
    # Get the coordinates of the not-NaN elements
    coords_not_nan = np.array(np.nonzero(not_nan)).T
    # Get the values of the not-NaN elements
    values_not_nan = arr[not_nan]
    # Get the coordinates of the elements to be interpolated
    coords_to_interp = np.array(np.nonzero(np.isnan(arr))).T
    # Perform the interpolation
    interp = NearestNDInterpolator(coords_not_nan, values_not_nan)
    interp_values = interp(coords_to_interp,k=1000, weights='distance')
    # Assign the interpolated values to the NaN elements in the original array
    arr[np.isnan(arr)] = interp_values
    return arr

def create_deformation_coords(deformation_arr):
    coords = np.mgrid[0:deformation_arr.shape[1], 0:deformation_arr.shape[2], 0:deformation_arr.shape[3]]
    deformed_coords = coords + deformation_arr
    return deformed_coords

def filter_out_of_bounds(coords):
    coords[0][coords[0]>=coords.shape[1]] = coords.shape[1] - 1
    coords[1][coords[1]>=coords.shape[2]] = coords.shape[2] - 1
    coords[2][coords[2]>=coords.shape[3]] = coords.shape[3] - 1
    coords[0][coords[0]<0] = 0
    coords[1][coords[1]<0] = 0
    coords[2][coords[2]<0] = 0
    return coords

def find_edge_nans(arr):
    # Assuming `img` is your image array
    mask = np.isnan(arr[0])
    # Create a mask for NaNs that are at the edge
    edge_mask = mask & ~binary_dilation(~mask)
    eroded_img = binary_erosion(edge_mask, structure=np.ones((3,3,3)))
    return eroded_img

def forward_transform(volume, forward_deformation):
    forward_coords = create_deformation_coords(forward_deformation)
    forward_coords = filter_out_of_bounds(forward_coords)
    forward_coords = np.round(forward_coords).astype(int)
    out_volume = np.zeros_like(volume)
    out_volume[:] = np.nan
    out_volume[:,forward_coords[0], forward_coords[1], forward_coords[2]] = -forward_coords 
    # Assuming `img` is your image array
    mask = find_edge_nans(out_volume)
    out_volume[:,~mask] = interpolate_array(out_volume[:,~mask])
    return out_volume


