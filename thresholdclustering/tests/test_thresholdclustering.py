import unittest
import community as community_louvain
import networkx as nx
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from thresholdclustering import best_partition


class CDTestCase(unittest.TestCase):

    def test_cd(self):

        # load the karate club graph
        G = nx.karate_club_graph()
        Adj=nx.to_numpy_matrix(G)
        cos_Adj=cosine_similarity(Adj.T)
        G=nx.from_numpy_matrix(cos_Adj)
        cluster_function = community_louvain.best_partition
        partition, alpha = best_partition(G, cluster_function=cluster_function)
        self.assertIsInstance(partition, dict)
        self.assertIsInstance(alpha, float)