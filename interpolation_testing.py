import numpy as np
from scipy.interpolate import NearestNDInterpolator
from scipy.interpolate.interpnd import _ndim_coords_from_arrays, NDInterpolatorBase

import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
rng = np.random.default_rng()

x = rng.random(10) - 0.5

y = rng.random(10) - 0.5

z = np.hypot(x, y)
X = np.linspace(min(x), max(x))

Y = np.linspace(min(y), max(y))

X, Y = np.meshgrid(X, Y)  # 2D grid for interpolation



method = 'distance'
interp = NearestNDInterpolator(list(zip(x, y)), z)
Z_ = interp(X, Y)

points = _ndim_coords_from_arrays((x, y))
# Create a KD-tree from the data points
tree = cKDTree(points)
#points = np.column_stack((X.ravel(), Y.ravel()))  # All points in the grid as (x, y) pairs
args = (X,Y)
xi = _ndim_coords_from_arrays(args, ndim=points.shape[1])
xi_flat = xi.reshape(-1, xi.shape[-1])
original_shape = xi.shape
flattened_shape = xi_flat.shape
# Query the KD-tree for nearest neighbor
dist, i = tree.query(xi_flat, k=1)
dist[0,0] = np.inf
valid_mask = np.isfinite(dist)
# Extract the values of the nearest neighbors
values = z[i]
if method=='distance':
    Z = np.average(values, axis=1, weights=dist)
elif method=='uniform':
    Z = np.average(values, axis=1)


# Plot
plt.figure(figsize=(8, 6))
plt.pcolor(X, Y, Z, shading='auto')
plt.plot(x, y, 'ko')  # Original data points
plt.colorbar()
plt.title('Nearest neighbor interpolation using KDTree')
plt.show()