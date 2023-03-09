import copy

import networkx as nx


def create_graph():
    """ Create an empty graph """

    graph = nx.Graph()

    return graph


def create_digraph():
    """ Create an empty digraph """

    digraph = nx.DiGraph()

    return digraph


def clone_graph(graph):
    """ Clone the given graph """

    clone_graph = copy.deepcopy(graph)

    return clone_graph


def get_order(graph):
    """ Get the order of a graph """

    order = len(graph.nodes)

    return order


def get_size(graph):
    """ Get the size of the graph """

    size = len(graph.edges)

    return size


def get_vertices(graph):
    """ Get the vertices of the graph """

    vertices = list(graph.nodes)

    return vertices


def get_min_vertex(graph):
    """ Get the value of the minimum vertex """

    minimum_vertex = np.min(graph.nodes)

    return minimum_vertex


def get_max_vertex(graph):
    """ Get the value of the maximum vertex """

    maximum_vertex = np.max(graph.nodes)

    return maximum_vertex


def get_all_edges(graph):
    """ Get all of the graph's edges """

    edges = list(graph.edges)

    return edges


def get_edge_weight(graph, edge):
    """ Get the weight associated with the given edge """

    weight = graph[edge[0]][edge[1]].get("weight")

    return weight


def get_edges_weights(graph, edges):
    """ Get the weights associated with the given edges """

    weights = [get_edge_weight(graph, edge) for edge in edges]

    return weights


def get_all_weights(graph):
    """ Get all of the edge weights for a given graph """

    edges = get_all_edges(graph)
    weights = [get_edge_weight(graph, edge) for edge in edges]

    return weights


def minimum_weight(graph, vertex, out=True):
    """ Compute minimum edge weight incident with vertex """

    weights = get_edge_weights(graph, vertex, out=out)
    minimum_weight = np.min(weights)

    return minimum_weight


def max_weight(graph, vertex, out=True):
    """ Compute maximum edge weight incident with vertex """

    weights = get_edge_weights(graph, vertex, out=out)
    maximum_weight = np.max(weights)

    return maximum_weight


def mean_weight(graph, vertex, out=True):
    """ Compute mean edge weight incident with vertex """

    weights = get_edge_weights(graph, vertex, out=out)
    mean_weight = np.mean(weights)

    return mean_weight


def store_edge_attribute(graph, edge, attribute, name):
    """ Store the given edge attribute with the given name at the given edge """

    graph[edge[0]][edge[1]][name] = attribute

    return graph


def store_edge_attributes(graph, edges, attributes, name):
    """ Store the given attributes for the given edges with the given name """

    attribute_dict = {edge: attribute for (edge, attribute) in zip(edges, attributes)}
    nx.set_edge_attributes(graph, values=attribute_dict, name=name)

    return graph


def store_node_attribute(graph, node, attribute, name):
    """ Store the given attribute with the given name at the given node """

    graph.nodes[node][name] = attribute

    return graph


def store_node_attributes(graph, nodes, attributes, name):
    """ Store the given node attributes at the given nodes """

    attribute_dict = {node: attribute for (node, attribute) in zip(nodes, attributes)}
    nx.set_node_attributes(graph, values=attribute_dict, name=name)

    return graph


def get_edge_attribute(graph, edge, name):
    """ Get the edge attribute with the given name """

    attribute = graph[edge[0]][edge[1]].get(name)

    return attribute


def get_edge_attributes(graph, edges, name):
    """ Get the edge attributes with the given name """

    attributes = [get_edge_attribute(graph, edge, name) for edge in edges]

    return attributes


def get_node_attribute(graph, node, name):
    """ Get the node attribute with the given name """

    attribute = graph.nodes[node].get(name)

    return attribute


def get_node_attributes(graph, nodes, name):
    """ Get the node attributes with the given name """

    attributes = [get_node_attribute(graph, node, name) for node in nodes]

    return attributes


def is_undirected(graph):
    """ Test if graph is undirected """

    if type(graph) == type(nx.Graph()):
        return True
    else:
        return False


def is_directed(graph):
    """ Test if graph is directed """

    if type(graph) == type(nx.DiGraph()):
        return True
    else:
        return False


def remove_node_from_graph(graph, node):
    """ Remove the node and all of its edges from the graph """

    prune_edges = [edge for edge in get_all_edges(graph) if node in edge]
    graph.remove_edges_from(prune_edges)
    graph.remove_nodes_from([node])

    return graph


def remove_nodes_from_graph(graph, nodes):
    """ Remove the nodes and all of their edges from the graph """

    for node in nodes:
        graph = remove_node_from_graph(graph, node)
    
    return graph


def build_graph_from_edges(edges, weights=None, symmetric=True):
    """ Using the given edges, build a graph with unit weights """

    if symmetric:
        graph = nx.Graph()
    else:
        graph = nx.DiGraph()
    weights = weights or [1, ] * len(edges)

    graph.add_edges_from(edges)

    return graph


def get_graph_metadata_dictionary(graph):
    """ Get the global graph metadata dictionary """

    metadata_dictionary = graph.graph

    return metadata_dictionary    


def set_graph_metadata_dictionary(graph, metadata_dictionary):
    """ Set  the global graph metadata dictionary """

    graph.graph = metadata_dictionary

    return graph


def set_graph_metadata_dictionary_element(graph, key, value):
    """ Set a key-value pair in the global graph metadata dictionary """

    graph.graph[key] = value

    return graph


def get_graph_coordinate_dictionary(graph):
    """ Get the global graph coordinate dictionary """

    metatdata_dictionary = get_graph_metadata_dictionary(graph)
    coordinate_dictionary = metatdata_dictionary.get("coord_dict")

    if coordinate_dictionary is None:
        raise ValueError("No coordinate dictionary found!")

    return coordinate_dictionary


def set_graph_coordinate_dictionary(graph, coordinate_dictionary):
    """ Set the global graph coordinate dictionary """

    graph = set_graph_metadata_dictionary_element(
        graph, "coord_dict", coordinate_dictionary
    )

    return graph


def get_node_coordinates(graph, node):
    """ Get the coordinates for the given node """

    coordinate_dictionary = get_graph_coordinate_dictionary(graph)
    coordinates = coordinate_dictionary.get(node)

    if coordinates is None:
        raise ValueError("No coordinates found for the given node!")

    return coordinates


def set_node_coordinates(graph, node, coordinates):
    """ Set the coordinates for the given node """

    coordinate_dictionary = get_graph_coordinate_dictionary(graph)
    coordinate_dictionary.update({node: coordinates})
    graph = set_graph_coordinate_dictionary(graph, coordinate_dictionary)
    
    return graph


def set_nodes_coordinates(graph, nodes, coordinates_iterable):
    """ Set the coordinates for the given nodes """

    for (node, coordinates) in zip(nodes, coordinates_iterable):
        graph = set_node_coordinates(graph, node, coordinates)

    return graph


def remove_node_coordinates(graph, node):
    """ Remove the node from the coordinate dictionary """

    coordinate_dictionary = get_graph_coordinate_dictionary(graph)
    _ = coordinate_dictionary.pop(node)
    graph = set_graph_coordinate_dictionary(graph, coordinate_dictionary)

    return graph


def remove_nodes_coordinates(graph, nodes):
    """ Remove the nodes from the coordinate dictionary """

    for node in nodes:
        graph = remove_node_coordinates(graph, node)

    return graph


def get_node_types_dictionary(graph):
    """ Get the node types for the given graph """

    metadata_dictionary = get_graph_metadata_dictionary(graph)
    node_types_dictionary = metadata_dictionary.get("node_types")

    if node_types_dictionary is None:
        raise ValueError("No node types specified!")

    return node_types_dictionary


def set_node_types_dictionary(graph, node_types_dictionary):
    """ Set the node types dictionary for the given graph """

    graph = set_graph_metadata_dictionary_element(
        graph, "node_types", node_types_dictionary
    )

    return graph


def get_depot_node(graph):
    """ Get the depot node for the given graph """

    depot_node = get_depot_nodes(graph)[0]
    
    return depot_node


def get_depot_nodes(graph):
    """ Get the depot nodes for the given graph """

    node_types = get_node_types_dictionary(graph)
    depot_nodes = node_types.get("depot")

    return depot_nodes


def get_customer_nodes(graph):
    """ Get the customer nodes for the given graph """

    node_types = get_node_types_dictionary(graph)
    customer_nodes = node_types.get("customer")

    return customer_nodes


def get_station_nodes(graph):
    """ Get the station nodes for the given graph """

    node_types = get_node_types_dictionary(graph)
    station_nodes = node_types.get("station")

    return station_nodes


def get_non_station_nodes(graph):
    """ Get the non-station nodes for the given graph """

    depot_nodes = get_depot_nodes(graph) or []
    customer_nodes = get_customer_nodes(graph) or []
    non_station_nodes = depot_nodes + customer_nodes

    return non_station_nodes


def set_depot_nodes(graph, depot_nodes):
    """ Set the depot nodes for the given graph """

    node_types_dictionary = get_node_types_dictionary(graph)
    node_types_dictionary["depot"] = depot_nodes
    graph = set_node_types_dictionary(graph, node_types_dictionary)

    return graph


def set_customer_nodes(graph, customer_nodes):
    """ Set the customer nodes for the given graph """

    node_types_dictionary = get_node_types_dictionary(graph)
    node_types_dictionary["customer"] = customer_nodes
    graph = set_node_types_dictionary(graph, node_types_dictionary)

    return graph


def set_station_nodes(graph, station_nodes):
    """ Set the station nodes for the given graph """

    node_types_dictionary = get_node_types_dictionary(graph)
    node_types_dictionary["station"] = station_nodes
    graph = set_node_types_dictionary(graph, node_types_dictionary)

    return graph


def remove_depot_node_type(graph, depot_node):
    """ Remove the given depot node from the node type list """

    depot_nodes = get_depot_nodes(graph)
    if depot_node in depot_nodes:
        _ = depot_nodes.pop(depot_nodes.index(depot_node))
        graph = set_depot_nodes(graph, depot_nodes)

    return graph


def remove_customer_node_type(graph, customer_node):
    """ Remove the given customer node from the node type list """

    customer_nodes = get_customer_nodes(graph)
    if customer_node in customer_nodes:
        _ = customer_nodes.pop(customer_nodes.index(customer_node))
        graph = set_customer_nodes(graph, customer_nodes)

    return graph


def remove_station_node_type(graph, station_node):
    """ Remove the given station node from the node type list """

    station_nodes = get_station_nodes(graph)
    if station_node in station_nodes:
        _ = station_nodes.pop(station_nodes.index(station_node))
        graph = set_station_nodes(graph, station_nodes)

    return graph


def remove_depot_node(graph, depot_node):
    """ Remove the depot node from the graph """

    graph = remove_depot_node_type(graph, depot_node)
    graph = remove_node_coordinates(graph, depot_node)
    graph = remove_node_from_graph(graph, depot_node)

    return graph


def remove_customer_node(graph, customer_node):
    """ Remove the customer node from the graph """

    graph = remove_customer_node_type(graph, customer_node)
    graph = remove_node_coordinates(graph, customer_node)
    graph = remove_node_from_graph(graph, customer_node)

    return graph


def remove_station_node(graph, station_node):
    """ Remove the station node from the graph """

    graph = remove_station_node_type(graph, station_node)
    graph = remove_node_coordinates(graph, station_node)
    graph = remove_node_from_graph(graph, station_node)

    return graph


def remove_depot_nodes(graph, depot_nodes=None):
    """ Remove the depot nodes from the graph """

    output_graph = clone_graph(graph)    
    depot_nodes = depot_nodes or get_depot_nodes(graph)
    for depot_node in depot_nodes:
        output_graph = remove_depot_node(output_graph, depot_node)

    return output_graph


def remove_customer_nodes(graph, customer_nodes=None):
    """ Remove the customer nodes from the graph """

    output_graph = clone_graph(graph)
    customer_nodes = customer_nodes or get_customer_nodes(graph)
    for customer_node in customer_nodes:
        output_graph = remove_customer_node(output_graph, customer_node)

    return output_graph


def remove_station_nodes(graph, station_nodes=None):
    """ Remove the station nodes from the graph """

    output_graph = clone_graph(graph)
    station_nodes = station_nodes or get_station_nodes(graph)
    for station_node in station_nodes:
        output_graph = remove_station_node(output_graph, station_node)

    return output_graph


def check_graph(graph):
    """ Check if the given graph is undirected """

    is_graph = type(graph) == nx.Graph

    return is_graph

def check_digraph(graph):
    """ Check of the graph is a directed graph """

    is_digraph = type(graph) == nx.DiGraph()

    return is_digraph
