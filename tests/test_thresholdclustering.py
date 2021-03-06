import community as community_louvain
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

#G = nx.small.krackhardt_kite_graph()
G = nx.les_miserables_graph()


import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity
# load the karate club graph
G = nx.karate_club_graph()
Adj=nx.to_numpy_matrix(G)
cos_Adj=cosine_similarity(Adj.T)
G=nx.from_numpy_matrix(cos_Adj)

pos = nx.spring_layout(G)
weights = np.array([G[u][v]['weight'] for u,v in G.edges()])*5
nx.draw_networkx_nodes(G, pos, node_size=40)
nx.draw_networkx_edges(G, pos, alpha=0.2, width=weights)
plt.show()


partition=community_louvain.best_partition(G.to_undirected())

cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
                       cmap=cmap, node_color=list(partition.values()))
nx.draw_networkx_edges(G, pos, alpha=0.2,width=weights)
plt.show()



from thresholdclustering.thresholdclustering import best_partition

cluster_function = community_louvain.best_partition
partition, alpha = best_partition(G, cluster_function=cluster_function)


# draw the graph
#pos = nx.spring_layout(G)
# color the nodes according to their partition
cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
                       cmap=cmap, node_color=list(partition.values()))
nx.draw_networkx_edges(G, pos, alpha=0.2,width=weights)
plt.show()

