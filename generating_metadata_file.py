from CCF_translator.deformation import apply_deformation, route_calculation 
import json
import pandas as pd
import networkx as nx

key_ages = [4,7,14,21,28,56]

file_name_template = "{}_pull_{}.nii.gz"

metadata_template = {
    "file_name":[],
    "source_space":[],
    "target_space":[],
    "dim_order":[],
}




metadata.iloc[10]


calculate_route('Demba_P56', 'Demba_P14', metadata)


new_metadata = []
for i,m in metadata[:].iterrows():
    if not m['target_key']:
        source_key = False
        magnitude_to_source = 0
    else:
        source_key = route_calculation.calculate_key_in_path(int(m['target_age_pnd']),int(m['source_age_pnd']),metadata[metadata['key_age']]['source_age_pnd'].values)
        magnitude_to_source = (source_key - m['source_age_pnd'])


    m['source_key'] = source_key           
    m['magnitude_to_source_key'] = magnitude_to_source      
    new_metadata.append(m)
                                      
metadata = pd.DataFrame(new_metadata)
new_metadata = []

for i,m in metadata[:].iterrows():
    if not m['target_key']:
        target_key = False
        magnitude_to_target = 0
    else:
        target_key = route_calculation.calculate_key_in_path(int(m['source_age_pnd']),int(m['target_age_pnd']),metadata[metadata['key_age']]['source_age_pnd'].values)
        magnitude_to_target = (target_key - m['source_age_pnd'])


    m['target_key'] = target_key           
    m['magnitude_to_target_key'] = magnitude_to_source    
    new_metadata.append(m)
                              
metadata = pd.DataFrame(new_metadata)
                 
metadata.loc[metadata['target_key_space'].str.contains('Demba', na=False), 'target_key_space'] = 'Demba'
#metadata.loc[metadata['source_key_space'].str.contains('Demba', na=False), 'source_key_space'] = 'Demba'
metadata.loc[metadata['target_space'].str.contains('Demba', na=False), 'target_space'] = 'Demba'
metadata.loc[metadata['source_space'].str.contains('Demba', na=False), 'source_space'] = 'Demba'
metadata.loc[metadata['target_key_space'].str.contains('Allen_CCF', na=False), 'target_key_space'] = 'Allen_CCF'
#metadata.loc[metadata['source_key_space'].str.contains('Allen_CCF', na=False), 'source_key_space'] = 'Allen_CCF'
metadata.loc[metadata['target_space'].str.contains('Allen_CCF', na=False), 'target_space'] = 'Allen_CCF'
metadata.loc[metadata['source_space'].str.contains('Allen_CCF', na=False), 'source_space'] = 'Allen_CCF'
