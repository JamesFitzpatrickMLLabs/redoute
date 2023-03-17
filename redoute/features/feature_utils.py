import torch

import numpy as np

from redoute.graph import problem_utils
from redoute.graph import graph_utils


def get_node_coordinate_array(graph):

    node_coordinates = problem_utils.get_node_coordinates(graph)
    node_coordinate_array = np.array(node_coordinates)

    return node_coordinate_array


def array_to_float_tensor(array):

    float_tensor = torch.tensor(array).float()

    return float_tensor



def sparsify_problem_graph_by_quantile(graph, quantile):

    copy_graph = graph_utils.clone_graph(graph)
    
    adjacency_matrix = get_adjacency_matrix_from_graph(graph)
    threshold = np.quantile(adjacency_matrix, quantile)
    edge_list = find_edges_greater_than_threshold(adjacency_matrix, threshold)
    edge_list = remove_edges_from_edge_list_if_depot_in_edge(edge_list)

    copy_graph.remove_edges_from(edge_list)

    return copy_graph


def sparsify_problem_graph_by_ordering(graph, neighbours):

    copy_graph = graph_utils.clone_graph(graph)
    
    adjacency_matrix = get_adjacency_matrix_from_graph(graph)
    threshold = np.sort(adjacency_matrix, -1)[:, neighbours + 1]
    edge_list = (np.argwhere(adjacency_matrix > threshold) + 1).tolist()
    edge_list = remove_edges_from_edge_list_if_depot_in_edge(edge_list)

    copy_graph.remove_edges_from(edge_list)

    return copy_graph
