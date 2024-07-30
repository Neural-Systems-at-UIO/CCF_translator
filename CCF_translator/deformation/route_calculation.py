import json
import networkx as nx
import numpy as np



def calculate_route(source, target, metadata):
    G = nx.DiGraph()
    for i,m in metadata.iterrows():
        s = m['source_space'] + '_P' + str(m['source_age_pnd'])
        t = m['target_space'] + '_P' +  str(m['target_age_pnd'])
        G.add_edge(s, t)
    path = nx.shortest_path(G, source, target)
    return path

def calculate_key_in_path(source, target, key_age_arr):
    direction = np.sign(target - source)
    if direction ==  -1:
        remaining_key_ages = key_age_arr[key_age_arr<int(source)]
        target_key = np.max(remaining_key_ages)
    if direction ==  1:
        remaining_key_ages = key_age_arr[key_age_arr>int(source)]
        target_key = np.min(remaining_key_ages)
    return target_key
    