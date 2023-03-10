from redoute.graph import graph_utils


def get_vehicle_capacity(graph):

    vehicle_capacity = graph.graph.get("vehicle_capacity")

    return vehicle_capacity


def get_node_demands(graph, nodes):

    node_demands = graph_utils.get_node_attributes(graph, nodes, "demand")

    return node_demands
