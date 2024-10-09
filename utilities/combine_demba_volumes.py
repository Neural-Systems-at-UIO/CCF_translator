# create a 4D volume for viewing in ITK snap

import nibabel as nib
import numpy as np
from glob import glob
import re

def extract_age(file_path):
    match = re.search(r'[/_]P(\d+)_', file_path)
    return int(match.group(1)) if match else float('inf')

paths =[
    "/home/harryc/github/CCF_translator/demo_data/demba_volumes/*demba_dev_mouse*",
        "/home/harryc/github/CCF_translator_local/demo_data/demba_20um/*allen_2022_annotation*",
        "/home/harryc/github/CCF_translator_local/demo_data/demba_20um/*allen_2017_annotation*",
        "/home/harryc/github/CCF_translator_local/demo_data/demba_20um/*kim_annotation*",
        "/home/harryc/github/demba_analysis/interpolated_gene/*calb1_gene_volume*",
        ]

for path in paths:
    name = path.split('/')[-1][1:-1]
    print(name)
    volume_list = glob(path)
    if len(volume_list) != 53:
        raise Exception("unexpected number of volumes")
    sorted_volumes = sorted(volume_list, key=extract_age)
    volumes = []
    for v in sorted_volumes:
        img = nib.load(v)
        arr = np.asanyarray(img.dataobj)
        volumes.append(arr)
    volumes = np.stack(volumes, axis=-1)
    if "annotation" not in path:
        #for memory reasons you may want to convert this to uint8
        volumes = volumes - np.min(volumes)
        volumes = volumes / np.max(volumes)
        volumes = volumes * 255
        volumes = volumes.astype(np.uint8)
    #it seems itk struggles to open such large time series so we instead split it in thirds
    nib.save(nib.Nifti1Image(volumes[:,:,:,:17], img.affine, img.header), f'../demo_data/{name}_P4_to_P20.nii.gz')
    nib.save(nib.Nifti1Image(volumes[:,:,:,17:34], img.affine, img.header), f'../demo_data/{name}_P21_to_P37.nii.gz')
    nib.save(nib.Nifti1Image(volumes[:,:,:,34:], img.affine, img.header), f'../demo_data/{name}_P38_to_P56.nii.gz')
    