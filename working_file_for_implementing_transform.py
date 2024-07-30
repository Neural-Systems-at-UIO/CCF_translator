from CCF_translator.deformation import apply_deformation, route_calculation 
import json
import pandas as pd
import networkx as nx

metadata_path = os.path.join("CCF_translator","metadata","translation_volume_info.json")
with open(metadata_path, 'r') as f:
    metadata = pd.DataFrame(json.load(f))
 

def calculate_route(source, target, metadata):
    # Load the JSON data
    # Create a directed graph
    G = nx.DiGraph()
    # Add nodes to the graph for each unique space
    spaces = set(metadata['source_space'] + metadata['target_key_space'])
    G.add_nodes_from(spaces)
    # Add edges to the graph for each transformation
    for i in range(len(metadata['file_name'])):
        G.add_edge(metadata['source_space'][i], metadata['target_key_space'][i])
    # Use the shortest_path function to find the shortest path between any two spaces
    path = nx.shortest_path(G, source=source, target=target)
    return path







# metadata.iloc[10]


# calculate_route('Demba_P56', 'Demba_P14', metadata)


# new_metadata = []
# for i,m in metadata[:].iterrows():
#     if not m['target_key']:
#         source_key = False
#         magnitude_to_source = 0
#     else:
#         source_key = route_calculation.calculate_key_in_path(int(m['target_age_pnd']),int(m['source_age_pnd']),metadata[metadata['key_age']]['source_age_pnd'].values)
#         magnitude_to_source = (source_key - m['source_age_pnd'])


#     m['source_key'] = source_key           
#     m['magnitude_to_source_key'] = magnitude_to_source      
#     new_metadata.append(m)
                                      
# metadata = pd.DataFrame(new_metadata)
# new_metadata = []

# for i,m in metadata[:].iterrows():
#     if not m['target_key']:
#         target_key = False
#         magnitude_to_target = 0
#     else:
#         target_key = route_calculation.calculate_key_in_path(int(m['source_age_pnd']),int(m['target_age_pnd']),metadata[metadata['key_age']]['source_age_pnd'].values)
#         magnitude_to_target = (target_key - m['source_age_pnd'])


#     m['target_key'] = target_key           
#     m['magnitude_to_target_key'] = magnitude_to_source    
#     new_metadata.append(m)
                              
# metadata = pd.DataFrame(new_metadata)
                 
# metadata.loc[metadata['target_key_space'].str.contains('Demba', na=False), 'target_key_space'] = 'Demba'
# #metadata.loc[metadata['source_key_space'].str.contains('Demba', na=False), 'source_key_space'] = 'Demba'
# metadata.loc[metadata['target_space'].str.contains('Demba', na=False), 'target_space'] = 'Demba'
# metadata.loc[metadata['source_space'].str.contains('Demba', na=False), 'source_space'] = 'Demba'
# metadata.loc[metadata['target_key_space'].str.contains('Allen_CCF', na=False), 'target_key_space'] = 'Allen_CCF'
# #metadata.loc[metadata['source_key_space'].str.contains('Allen_CCF', na=False), 'source_key_space'] = 'Allen_CCF'
# metadata.loc[metadata['target_space'].str.contains('Allen_CCF', na=False), 'target_space'] = 'Allen_CCF'
# metadata.loc[metadata['source_space'].str.contains('Allen_CCF', na=False), 'source_space'] = 'Allen_CCF'

G = nx.DiGraph()
# Add nodes to the graph for each unique space
spaces = set(metadata['source_space'].tolist() + metadata['target_key_space'].tolist())
#G.add_nodes_from(spaces)
for i,m in metadata[:].iterrows():
    if False in m[['source_key', 'target_key']].values:
        G.add_edge(f"{m['source_space']}_P{m['source_age_pnd']}", f"{m['target_space']}_P{m['source_age_pnd']}" )
        continue
    start = m[['source_key', 'target_key']].min()
    stop = m[['source_key', 'target_key']].max()
    
    for i in range(start,stop+1):
        if i == m['source_age_pnd']:
            continue
        G.add_edge(f"{m['source_space']}_P{m['source_age_pnd']}", f"{m['target_space']}_P{i}" )
nx.shortest_path(G, source='Allen_CCF_P56', target='Demba_P5')

# with open('metadata.json', 'w') as f:
#     json.dump(metadata.to_dict('list'),f)

new_metadata = []
for i,m in metadata[:].iterrows():
    new_values = m.copy()
    if False in m[['source_key', 'target_key']].values:
        new_metadata.append(m)
        #G.add_edge(f"{m['source_space']}_P{m['source_age_pnd']}", f"{m['target_space']}_P{m['source_age_pnd']}" )
        continue
    start = m[['source_key', 'target_key']].min()
    stop = m[['source_key', 'target_key']].max()
    
    for i in range(start,stop+1):
        if i == m['source_age_pnd']:
            continue
        new_values['target_age_pnd'] = i
        orignal_valence = np.sign(m['target_age_pnd'] - new_values['source_age_pnd'])
        new_valence = np.sign(new_values['target_age_pnd'] - new_values['source_age_pnd'])
        new_magnitude = np.abs(new_values['target_age_pnd'] - new_values['source_age_pnd'])
        if original_valence != new_valence:
            new_magnitude *= 1
        #G.add_edge(f"{m['source_space']}_P{m['source_age_pnd']}", f"{m['target_space']}_P{i}" )

