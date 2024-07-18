
import CCF_translator as CCFT
import nibabel as nib
import numpy as np
import json
#import h5py
#import hdf5plugin
import scipy
import networkx as nx
import matplotlib.pyplot as plt

def create_deformation_coords(deformation_arr):
    coords = np.mgrid[0:deformation_arr.shape[1], 0:deformation_arr.shape[2], 0:deformation_arr.shape[3]]
    deformed_coords = coords + deformation_arr
    return deformed_coords

def calculate_route(source, target):
    # Load the JSON data
    # Create a directed graph
    G = nx.DiGraph()
    # Add nodes to the graph for each unique space
    spaces = set(metadata['source_space'] + metadata['target_space'])
    G.add_nodes_from(spaces)
    # Add edges to the graph for each transformation
    for i in range(len(metadata['file_name'])):
        G.add_edge(metadata['source_space'][i], metadata['target_space'][i], weight=1)
    # Use the shortest_path function to find the shortest path between any two spaces
    path = nx.shortest_path(G, source=source, target=target, weight='weight')
    return path

def open_transformation(transform_path, selected_data):
    deformation_img = nib.load(transform_path + selected_data['file_name'][0])
    deformation = deformation_img.get_fdata()
    magnitude = selected_data['translation_magnitude'][0]
    deformation = deformation / (magnitude )
    deformation =  np.transpose(deformation, (3,0,1,2))
    return deformation

def apply_transform(data, deformation, order, apply_to_coords = False):
    deformation_coords = create_deformation_coords(deformation)
    out_data = np.empty(data.shape)
    if apply_to_coords:
        for i in range(data.shape[0]):
            out_data[i] = scipy.ndimage.map_coordinates(data[i], deformation_coords, order=order)
    else:
        out_data = scipy.ndimage.map_coordinates(data, deformation_coords, order=order)
    return out_data

def calculate_nearest_template(current_age, target_age, metadata, calculate_for):
    diff = target_age - current_age
    direction = np.sign(diff)
    ages = np.unique(metadata["source_age_pnd"] + metadata["target_age_pnd"])
    if calculate_for=="current":
        distances_to_template = -(current_age - ages)
    elif calculate_for=="target":
        distances_to_template = -(target_age - ages)
    distances_to_template_ages = {
        a: i
        for a, i in zip(ages, distances_to_template)
        #if (np.sign(i) == direction or i == 0)
    }
    values = np.array(list(distances_to_template_ages.values())).astype(float)
    mask = np.sign(values) != np.sign(direction)
    values[mask] = np.inf  # assign a high value to the ones that don't match the sign
    min_pos = np.argmin(np.abs(values))
    keys = list(distances_to_template_ages.keys())
    nearest_template = keys[min_pos]
    prev_template = keys[min_pos - direction]
    #diff_to_template = current_age - nearest_template
    return prev_template, nearest_template

def transform_to_key_age(CCFT_vol, nearest_template, prev_template, metadata, order=0):
    mask = (np.array(metadata["source_age_pnd"]) == prev_template) & (
            np.array(metadata["target_age_pnd"]) == nearest_template
        )
    selected_data = {key: np.array(val)[mask] for key, val in metadata.items()}
    deformation = open_transformation(metadata_path, selected_data)
    ###I think these could cause a bug if the direction is opposite
    diff_to_current_age = selected_data['source_age_pnd'] - CCFT_vol.current_age
    #deformation = apply_transform(deformation, deformation * diff_to_current_age, 1, apply_to_coords=True)
    diff_to_target = CCFT_vol.current_age - selected_data["target_age_pnd"]
    #I think we are not properly calculating diff to target
    print(diff_to_target)
    CCFT_vol.values = apply_transform(CCFT_vol.values, deformation * diff_to_target, order, apply_to_coords=False)
    CCFT_vol.current_age = selected_data['target_age_pnd'][0]
    return CCFT_vol

def transform_age(CCFT_vol, target_age, order=0):
    order = 0

    if CCFT_vol.current_age not in metadata['source_age_pnd']:
        prev_template, nearest_template = calculate_nearest_template(current_age, target_age, metadata, "current")
        CCFT_vol = transform_to_key_age(CCFT_vol,nearest_template,prev_template, metadata,order=order)
    """THIS IS A TEST THAT WILL ONLY WORK FOR an age between 28 and 56 to 28"""
    if target_age not in metadata['source_age_pnd']:
        prev_template, nearest_template = calculate_nearest_template(current_age, target_age, metadata, "target")
        mask = (np.array(metadata["source_age_pnd"]) == prev_template) & (
            np.array(metadata["target_age_pnd"]) == nearest_template
            )
        selected_data = {key: np.array(val)[mask] for key, val in metadata.items()}
        deformation = open_transformation(metadata_path, selected_data)
        CCFT_vol.values = apply_transform(CCFT_vol.values, deformation, order, apply_to_coords=False)
    return CCFT_vol





age = 55
target_age = 28

# Load the image
image = nib.load(f"demo_data/DeMBA_P{age}_segmentation_2022.nii.gz")
volume =  np.array(image.dataobj)
metadata_filepath = r"CCF_translator/metadata/translation_volume_info.json"
with open(metadata_filepath) as f:
    metadata = json.load(f)
space_metadata_filepath = r"CCF_translator/metadata/space_info.json"
with open(space_metadata_filepath) as f:
    space_metadata = json.load(f)

metadata_path = r"CCF_translator/metadata/deformation_fields/allen_mouse_CCF/" 


# Create a CCFT object
# this can be done for either volumes or points
# for volumes we would run the following
CCFT_vol = CCFT.volume(data=volume, 
                       space="CCFv3", 
                       voxel_size_um=20, 
                       age_PND=age, 
                       segmentation_file=True)

current_age = CCFT_vol.current_age
print(current_age)

order = 0


CCFT_vol = transform_age(CCFT_vol, target_age=target_age, order=0)


# if target_age not in space_metadata['total_spaces']:
#      prev_template, nearest_template = calculate_nearest_template(current_age, target_age, metadata, "target")

# alternatively for points we could do this
# with open("my_points.txt") as f:
#     points = np.array(f.readlines())
# CCFT_pts = CCFT.create_pointset(points, space="CCFv3", voxel_size_um=20, age_PND=31)

# we can then translate either the points or volumes into a new target age or space.
# CCFT will try to find a path from the current space into the target one
# CCFT_vol.translate(target_age=56)
# # the API is the same for points
# CCFT_pts.translate(target_age=56)
# # To check the current age of any CCFT object run
# print(CCFT_vol.current_age)  # -> P56
# # To check the original age of any object run
# print(CCFT_vol.original_age)  # -> P31

data = CCFT_vol.values
#save data
img = nib.Nifti1Image(data, image.affine, header=image.header)



nib.save(img, f"demo_data/DeMBA_P{target_age}_seg_warp2.nii.gz")




