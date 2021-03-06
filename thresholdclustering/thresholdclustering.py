from typing import Union, Optional

import networkx as nx
import numpy as np
import typing


def best_partition(G: Union[nx.DiGraph, nx.Graph], starting_alpha: Optional[float] = 0.1, threshold_function: Optional[
    typing.Callable] = np.mean, cluster_function: Optional[typing.Callable] = None,
                   weight: Optional[str] = "weight") -> tuple:
    """
    Returns the best partition according to cluster_function or, if not given, components in the transformed network.

    The directed, weighted graph is pruned with threshold_function, applied locally to the out-degree, and an increasing, scaled alpha parameter, until
    the algebraic connectivity goes to zero, that is, the network is no longer connected. Isolates are not counted.

    Returns a partition dictionary, and the alpha parameter used to create it.


    Parameters
    ----------
    G: Union[nx.DiGraph, nx.Graph]
        Graph
    starting_alpha: float, optional
        Starting value, incremented in 0.1 steps until transformed network is disconnected. Default is 0.1
    threshold_function: callable, optional
        Ties smaller than threshold_function(out_ties) are deleted. Example: np.mean, np.median. Default is np.mean.
    cluster_function: callable, optional
        Community detection function applied to the transformed undirected graph.
        If None, components of transformed graph are returned. Default is None.
    weight: str, optional
        Weight parameter. Default is 'weight'.

    Returns
    -------
    Tuple of
        partition: dict
            Partition of form {node: cluster_id} where max(cluster_id) is the set of isolate nodes
        alpha: float
            Last used alpha parameter

    """
    alpha = starting_alpha
    is_connected = True
    # Proceed until connectivity is zero
    while is_connected:

        # Require directed graph
        if G.is_directed() is False:
            G = G.to_directed()

        # Transformed graph
        new_graph = nx.Graph()


        # Consider all neighborhoods
        for node, neighbors in G.adjacency():
            weights = np.array([x[weight] for x in neighbors.values()])
            # Local threshold
            threshold = threshold_function(weights) + alpha * np.std(weights)
            for alter in neighbors:
                # Bidirected edges weight = 1, unidirected edges weight = 0.5
                if neighbors[alter][weight] >= threshold and (node != alter):
                    if new_graph.has_edge(node, alter):
                        new_graph[node][alter][weight] = 1
                    else:
                        new_graph.add_edges_from([(node, alter, {weight: 0.5})])

        # Increase alpha
        alpha += 0.1

        nr_comp = len(list(nx.connected_components(new_graph)))
        if nr_comp > 1 or alpha > 100:
            is_connected = False

    # Community detection
    if cluster_function is None:
        # Simply return connected components
        partition = {}
        for i, component in enumerate(nx.connected_components(new_graph)):
            partition.update({x: i + 1 for x in component})
    else:
        # Run a cluster function
        partition = cluster_function(new_graph)
        assert isinstance(partition, dict), "The cluster_function must return a dictionary of form {node:int}!"
    # Add isolates
    isolates = np.setdiff1d(G.nodes, new_graph.nodes)
    partition.update({x: np.max(list(partition.values())) + 1 for x in isolates})

    return partition, alpha
