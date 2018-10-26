import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

G.add_nodes_from([1, 2, 3, 4])
G.add_edges_from([(1, 2), (2, 1), (2, 3)])
H = nx.relabel_nodes(G, {1: 'one', 2: 'two', 3: 'three', 4: 'four'})
nx.draw(H, with_labels=True)
plt.savefig("graph.png")
plt.show()