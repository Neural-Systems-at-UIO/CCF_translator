import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import numpy as np
import CCF_translator
scale = 2.5
# points = np.array([(908, 342, 287)]) / scale
points = np.array([(1195, 268, 575)]) / scale
# points = np.array([(1320, 800, 1140)]) / scale
# points -= 1
# target = 'perens_stpt_mouse'
# pset = CCF_translator.Pointset(points, 'allen_mouse', voxel_size_micron=25, age_PND=56)
# pset.transform(target_age=56, target_space=target)
# print(f"{target}: new points are {pset.values * scale}")

# target = 'demba_dev_mouse'
# pset = CCF_translator.Pointset(points, 'allen_mouse', voxel_size_micron=25, age_PND=56)
# pset.transform(target_age=56, target_space=target)
# print(f"{target}: new points are {pset.values * scale}")


target = 'perens_lsfm_mouse'
pset = CCF_translator.Pointset(points, 'allen_mouse', voxel_size_micron=25, age_PND=56)
pset.transform(target_age=56, target_space=target)
print(f"{target}: new points are {pset.values * scale}")



target = 'perens_mri_mouse'
pset = CCF_translator.Pointset(points, 'allen_mouse', voxel_size_micron=25, age_PND=56)
pset.transform(target_age=56, target_space=target)
print(f"{target}: new points are {pset.values * scale}")


target = 'demba_dev_mouse'
pset = CCF_translator.Pointset(points, 'allen_mouse', voxel_size_micron=25, age_PND=56)
pset.transform(target_age=32, target_space=target)
print(f"{target}: new points are {pset.values * scale}")

print(r"correct result is 566, 1374, 483")
# [138.72000122 419.95246887 200.84948206]
# pset = CCF_translator.Pointset(points, 'perens_lsfm_mouse', voxel_size_micron=20, age_PND=56)
# pset.transform(target_age=56, target_space='allen_mouse')
# print(f"new points are {pset.values}")

