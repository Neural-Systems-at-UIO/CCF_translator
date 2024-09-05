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
