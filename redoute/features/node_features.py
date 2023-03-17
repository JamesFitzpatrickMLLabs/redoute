import numpy as np

from redoute.features import feature_utils


def compute_node_coordinate_features(graph, x_min=None, x_max=None, y_min=None, y_max=None):

    node_coordinate_array = feature_utils.get_node_coordinate_array(graph)
    if x_min is None:
        x_min = node_coordinate_array[..., 0].min()
    if x_max is None:
        x_max = node_coordinate_array[..., 0].max()
    if y_min is None:
        y_min = node_coordinate_array[..., 1].min()
    if y_max is None:
        y_max = node_coordinate_array[..., 1].max()
    diff = max([x_max - x_min, y_max - y_min])
    node_coordinate_array[..., 0] -= x_min
    node_coordinate_array[..., 0] /= diff
    node_coordinate_array[..., 1] -= y_min
    node_coordinate_array[..., 1] /= diff

    return node_coordinate_array
