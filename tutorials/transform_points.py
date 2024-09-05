import os

os.chdir("..")

import numpy as np
import CCF_translator

multi_point = np.array([(286, 250, 267), (414, 247, 452)])
pset = CCF_translator.pointset(
    multi_point, "demba_dev_mouse", voxel_size_micron=20, age_PND=56
)
pset.transform(target_age=56, target_space="allen_mouse")
print(pset.values)
