import json
import networkx as nx
import numpy as np

def calculate_route(source, target, metadata):
    # Load the JSON data
    # Create a directed graph
    G = nx.DiGraph()
    # Add nodes to the graph for each unique space
    spaces = set(metadata['source_space'] + metadata['target_key_space'])
    G.add_nodes_from(spaces)
    # Add edges to the graph for each transformation
    for i in range(len(metadata['file_name'])):
        G.add_edge(metadata['source_space'][i], metadata['target_key_space'][i], weight=1)
    # Use the shortest_path function to find the shortest path between any two spaces
    path = nx.shortest_path(G, source=source, target=target, weight='weight')
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
    