# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import matplotlib.pyplot as ml
import networkx as nx
import os as os
import json as json
from networkx.readwrite import json_graph
from pprint import pprint

path_to_json = '.'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
G = nx.Graph()

for x in range(250):
    G.add_node(json_files[x][:len(json_files[x]) - 5])
#print(G.nodes())

for x in range(250):
    with open(json_files[x], encoding='utf-8') as f:
        js_graph = json.load(f)

    for i in range(len(js_graph['Names'])):
        G.add_edge(json_files[x][:len(json_files[x]) - 5], js_graph['Names'][i])

#nx.write_graphml(G)
#print(G.edges())
graph_pos = nx.shell_layout(G)
nx.draw_networkx_nodes(G, graph_pos, node_size=250)
nx.draw_networkx_edges(G, graph_pos)
nx.draw_networkx_labels(G, graph_pos)
ml.show()