# threshold-clustering

## Threshold Spectral Community Detection for NetworkX


NetworkX Community detection based on the algorithm proposed in Guzzi et. al. 2013 (*).

Developed for semantic similarity networks, this algorithm specifically targets weighted and directed graphs. 
This implementation adds a couple of options to the algorithm proposed in the paper, such as passing an arbitrary community detection function (e.g. python-louvain).

Similarity networks are typically dense, weighted and difficult to cluster. Experience shows that algorithms such as python-louvain 
have difficulty finding outliers and smaller partitions.

Given a networkX.DiGraph object, threshold-clustering will try to remove insignificant ties according to a local threshold.
This threshold is refined until the network breaks into distinct components in a sparse, undirected network.

As a next step, either these components are taken communities directly, or, alternatively, another community detection (e.g. python-louvain)
can be applied.


## Example

Consider the cosine similarities in the Karate Club Network. Although these similarities are not directed, they are rather dense.

```python
import networkx as nx
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

# load graph
G = nx.karate_club_graph()

# Generate a similarity style weighted graph
Adj=nx.to_numpy_matrix(G)
cos_Adj=cosine_similarity(Adj.T)
G=nx.from_numpy_matrix(cos_Adj)

pos = nx.spring_layout(G)
weights = np.array([G[u][v]['weight'] for u,v in G.edges()])*5
nx.draw_networkx_nodes(G, pos, node_size=40)
nx.draw_networkx_edges(G, pos, alpha=0.2, width=weights)
plt.show()
```


![Similarity Network](https://raw.githubusercontent.com/IngoMarquart/python-threshold-clustering/main/nw1.png)

Let's use python-louvain to find the best partition.

```python
partition=community_louvain.best_partition(G.to_undirected())

cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
                       cmap=cmap, node_color=list(partition.values()))
nx.draw_networkx_edges(G, pos, alpha=0.2,width=weights)
plt.show()
```

![Best Partition](https://raw.githubusercontent.com/IngoMarquart/python-threshold-clustering/main/nw4.png)

We get three rather large partition and no sense of outliers.

Instead, we can use threshold-clustering's best_partition function to run python_louvain's community detection on a
transformed network. 


```python
from thresholdclustering import best_partition

cluster_function = community_louvain.best_partition
partition, alpha = best_partition(G, cluster_function=cluster_function)



cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
                       cmap=cmap, node_color=list(partition.values()))
nx.draw_networkx_edges(G, pos, alpha=0.2,width=weights)
plt.show()
```


![Best Partition with threshold-clustering](https://raw.githubusercontent.com/IngoMarquart/python-threshold-clustering/main/nw3.png)


We can see that more communities of similarity can be identified. Note in particular outliers drawn in yellow.


## Installation



`(*) Guzzi, Pietro Hiram, Pierangelo Veltri, and Mario Cannataro. "Thresholding of semantic similarity networks using a spectral graph-based technique." 
International Workshop on New Frontiers in Mining Complex Patterns. Springer, Cham, 2013.`


