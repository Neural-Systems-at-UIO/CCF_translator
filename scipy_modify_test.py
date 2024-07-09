from KNearestNDInterpolator import NearestNDInterpolator
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng()
x = rng.random(1000) - 0.5
y = rng.random(1000) - 0.5
z = np.hypot(x, y)
X = np.linspace(min(x), max(x))
Y = np.linspace(min(y), max(y))
X, Y = np.meshgrid(X, Y)  # 2D grid for interpolation
interp = NearestNDInterpolator(list(zip(x, y)), z)
Z_ = interp(X, Y, k=1)
# Plot
plt.figure(figsize=(8, 6))
plt.pcolor(X, Y, Z_, shading='auto')
#plt.plot(x, y, 'ko')  # Original data points
plt.colorbar()
plt.title('Nearest neighbor interpolation using KDTree')
plt.show()


print('passed case of k=1')
Z_ = interp(X, Y, k=200, weights='distance')
print('passed case of k=2')
# Plot
plt.figure(figsize=(8, 6))
plt.pcolor(X, Y, Z_, shading='auto')
#plt.plot(x, y, 'ko')  # Original data points
plt.colorbar()
plt.title('Nearest neighbor interpolation using KDTree')
plt.show()



