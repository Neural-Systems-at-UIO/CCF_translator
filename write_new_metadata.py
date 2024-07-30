from glob import glob
import json
import os
import numpy as np
files = glob(r"/home/harryc/github/CCF_translator/CCF_translator/metadata/deformation_fields/allen_mouse_CCF/*.nii.gz")
key_ages = ['4', '7', '14', '21', '28', '56']
metadata = {
    "file_name":[],
    "source_space":[],
    "target_space":[],
    "source_age_pnd":[],
    "target_age_pnd":[],
    "translation_magnitude":[],
    "transformation_resolution_micron":[],
    "key_age":[],
    "target_key":[],
    "target_key_space":[],
    "magnitude_to_key":[]
}
for file in files:
    file_name = os.path.basename(file)
    base = file_name.split('.')[0]
    source, dir, target = base.split('_')
    if source in key_ages:
        key = True
    else:
        key = False

    metadata["file_name"].append(file_name)
    metadata["source_space"].append(f"allen_mouse_CCF_P{source}")
    metadata["target_space"].append(f"allen_mouse_CCF_P{target}")
    metadata["source_age_pnd"].append(int(source)),
    metadata["target_age_pnd"].append(int(target)),
    metadata["translation_magnitude"].append(abs(int(source) - int(target)))
    metadata["key_age"].append(key)
    metadata["transformation_resolution_micron"].append(20)
    direction = np.sign(int(target)- int(source))
    key_age_arr = np.array(key_ages).astype(int)
    if direction ==  -1:
        remaining_key_ages = key_age_arr[key_age_arr<int(source)]
        target_key = np.max(remaining_key_ages)
    if direction ==  1:
        remaining_key_ages = key_age_arr[key_age_arr>int(source)]
        target_key = np.min(remaining_key_ages)
    metadata["target_key"].append(int(target_key))
    metadata["target_key_space"].append('allen_mouse_CCF_P' + str(target_key))
    metadata["magnitude_to_key"].append(abs(int(target_key) - int(source)))





with open(r"/home/harryc/github/CCF_translator/CCF_translator/metadata/translation_volume_info.json", 'w') as f:
    json.dump(metadata, f) 


