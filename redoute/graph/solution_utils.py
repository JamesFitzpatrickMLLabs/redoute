from redoute.graph import graph_utils


def get_route_edges(route):

    route_edges = [
        (a, b) for (a, b) in zip(route[:-1], route[1:])
    ]

    return route_edges
