import json
import networkx as nx

def calculate_route(source, target)
    # Load the JSON data
    with open("../metadata/translation_volume_info.json") as f:
        data = json.load(f)
    # Create a directed graph
    G = nx.DiGraph()
    # Add nodes to the graph for each unique space
    spaces = set(data['source_space'] + data['target_space'])
    G.add_nodes_from(spaces)
    # Add edges to the graph for each transformation
    for i in range(len(data['file_name'])):
        G.add_edge(data['source_space'][i], data['target_space'][i], weight=1)
    # Use the shortest_path function to find the shortest path between any two spaces
    path = nx.shortest_path(G, source=source, target=target, weight='weight')
    return path

def transform_to_nearest(source, target, data):
    