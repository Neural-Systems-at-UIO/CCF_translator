import json
import networkx as nx
import numpy as np


def calculate_route(source, target, metadata):
    G = nx.DiGraph()
    for i, m in metadata.iterrows():
        s = m["source_space"] + "_P" + str(m["source_age_pnd"])
        t = m["target_space"] + "_P" + str(m["target_age_pnd"])
        G.add_edge(s, t)
    path = nx.shortest_path(G, source, target)
    return path

def find_hamiltonian_path(metadata):
    G = nx.DiGraph()
    for i, m in metadata.iterrows():
        s = m["source_space"] + "_P" + str(m["source_age_pnd"])
        t = m["target_space"] + "_P" + str(m["target_age_pnd"])
        G.add_edge(s, t)
    
    def backtrack(path):
        if len(path) == len(G):
            return path
        for neighbor in G.neighbors(path[-1]):
            if neighbor not in path:
                path.append(neighbor)
                result = backtrack(path)
                if result:
                    return result
                path.pop()
        return None

    for node in G.nodes():
        path = backtrack([node])
        if path:
            return path
    return None