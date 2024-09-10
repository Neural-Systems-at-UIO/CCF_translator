import os
import sys
sys.path.append(os.path.abspath("/home/harryc/github/CCF_translator/"))

from CCF_translator import Series

data = {
    'values'
}

CCFT_vol = CCF_translator.Volume(
    values=atlas.reference,
    space="princeton_mouse",
    voxel_size_micron=voxel_size_micron,
    segmentation_file=False,
    age_PND=source_age,
)