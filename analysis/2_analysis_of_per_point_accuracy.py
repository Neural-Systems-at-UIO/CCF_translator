import pandas as pd
import os
os.chdir('..')
import numpy as np
import matplotlib.pyplot as plt
from CCF_translator.deformation.interpolation.NearestNDInterpolator import NearestNDInterpolator
import nibabel as nib

def interpolate_volume(volume, mask):
    # Get the shape of the volume
    shape = volume.shape
    # Create a grid of points in the volume
    grid = np.mgrid[0:shape[0], 0:shape[1], 0:shape[2]]
    points = grid.reshape((3, -1)).T
    # Flatten the volume
    mask = mask.flatten()
    values = volume.flatten()
    nan_pos = np.isnan(values)
    interp_mask = ~nan_pos & mask
    # Create the interpolator
    interpolator = NearestNDInterpolator(points[interp_mask], values[interp_mask])
    # Interpolate the volume
    out_mask = nan_pos & mask
    values[out_mask] = interpolator(points[out_mask], k=30, weights='distance')
    # Reshape the interpolated volume to the original shape
    interpolated_volume = values.reshape(shape)
    return interpolated_volume

threshold = 70
volume_shape = (570, 400, 705)
key_ages = [56, 28, 21, 14, 7, 4]
for age in key_ages:
    points = pd.read_csv(rf"demo_data/individual_P{age}.csv")
    annotation = nib.load(rf"/mnt/z/HBP_Atlasing/Developmental_atlases/DeMBA_Developmental mouse brain atlas/DeMBA-v1/01_working-environment/01_Data/DeMBA_v1/interpolated_segmentations/AllenCCFv3_segmentations/DeMBA_P{age}_segmentation_2022.nii.gz")
    annotation_vol = np.asanyarray(annotation.dataobj)
    distances  = points[['Distance Ingvild to Heidi', 'Distance Heidi to Demba','Distance Ingvild to Demba' ]]
    mask = [(points['Heidi x']>0) & (points['Ingvild x']>0) & (points['Demba x']>0) & (points['Heidi x'] < volume_shape[0]) 
            & (points['Ingvild x'] < volume_shape[0]) & (points['Demba x'] < volume_shape[0]) & (points['Heidi y']>0) & (points['Ingvild y']>0) & (points['Demba y']>0) & (points['Heidi y'] < volume_shape[1]) 
            & (points['Ingvild y'] < volume_shape[1]) & (points['Demba y'] < volume_shape[1]) & (points['Heidi z']>0) & (points['Ingvild z']>0) & (points['Demba z']>0) & (points['Heidi z'] < volume_shape[2])
            & (points['Ingvild z'] < volume_shape[2]) & (points['Demba z'] < volume_shape[2]) & distances['Distance Ingvild to Heidi']<threshold]
    distances = distances[mask[0]]
    points = points[mask[0]]
    volume = np.zeros(volume_shape)
    volume[:] = np.nan
    t_points = np.round(points[['Demba x', 'Demba y', 'Demba z']]).astype(int).values
    volume[t_points[:,0], t_points[:,1], t_points[:,2]] = distances[['Distance Ingvild to Demba', 'Distance Heidi to Demba']].mean(axis=1)
    volume = interpolate_volume(volume, annotation_vol!=0)
    out_img = nib.Nifti1Image(volume, annotation.affine, annotation.header)
    nib.save(out_img, f'demo_data/demba_{age}_error_volume.nii.gz')
    break
for age in key_ages:
    points = pd.read_csv(rf"demo_data/individual_P{age}.csv")
    annotation = nib.load(rf"/mnt/z/HBP_Atlasing/Developmental_atlases/DeMBA_Developmental mouse brain atlas/DeMBA-v1/01_working-environment/01_Data/DeMBA_v1/interpolated_segmentations/AllenCCFv3_segmentations/DeMBA_P{age}_segmentation_2022.nii.gz")
    annotation_vol = np.asanyarray(annotation.dataobj)
    distances  = points[['Distance Ingvild to Heidi']]
    mask = [(points['Heidi x']>0) & (points['Ingvild x']>0)  & (points['Heidi x'] < 570) 
            & (points['Ingvild x'] < 570)  & (points['Heidi y']>0) & (points['Ingvild y']>0)  & (points['Heidi y'] < 400) 
            & (points['Ingvild y'] < 400) & (points['Heidi z']>0) & (points['Ingvild z']>0)  & (points['Heidi z'] < 705)
            & (points['Ingvild z'] < 705) & distances['Distance Ingvild to Heidi']<threshold]
    distances = distances[mask[0]]
    points = points[mask[0]]
    volume = np.zeros(volume_shape)
    volume[:] = np.nan
    t_points = np.round(points[['Demba x', 'Demba y', 'Demba z']]).astype(int).values
    volume[t_points[:,0], t_points[:,1], t_points[:,2]] = distances['Distance Ingvild to Heidi']
    volume = interpolate_volume(volume, annotation_vol!=0)
    out_img = nib.Nifti1Image(volume, annotation.affine, annotation.header)
    nib.save(out_img, f'demo_data/heidi_ingvild_{age}_error_volume.nii.gz')
    break