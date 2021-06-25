import community as community_louvain
import networkx as nx
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from thresholdclustering import best_partition

G = nx.les_miserables_graph()

# load the karate club graph
G = nx.karate_club_graph()
Adj=nx.to_numpy_matrix(G)
cos_Adj=cosine_similarity(Adj.T)
G=nx.from_numpy_matrix(cos_Adj)

pos = nx.spring_layout(G)
weights = np.array([G[u][v]['weight'] for u, v in G.edges()])*5
partition=community_louvain.best_partition(G.to_undirected())
cluster_function = community_louvain.best_partition
partition, alpha = best_partition(G, cluster_function=cluster_function)
