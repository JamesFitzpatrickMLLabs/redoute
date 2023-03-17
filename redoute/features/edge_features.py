import numpy as np

from redoute.feature import feature_utils
from redoute.graph import graph_utils


def compute_global_relative_edge_weight_feature(graph):

    edge_weights = graph_utils.get_edges_weights(graph, graph.edges)
    global_relative_edge_weight = np.array(edge_weights) / max(edge_weights)

    return global_relative_edge_weight
