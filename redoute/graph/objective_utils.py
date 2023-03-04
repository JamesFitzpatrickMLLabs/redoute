from optlearn.graph import solution_utils


class objectiveComputer():

    def __init__(self, route_objective_calculator):

        self._route_objective_calculator = route_objective_calculator

    def _get_routes(self, solution):

        if self._check_contains_lists(solution):
            routes = solution
        else:
            routes = [solution]

        return routes
    
    def _check_contains_lists(self, solution):

        contains_lists = any([
            isinstance(list, item) for item in solution
        ])

        return contains_lists

    def _compute_route_cost(self, graph, route):

        route_cost = self._route_objective_calculator(graph, route)
        
        return route_cost

    def _compute_routes_costs(self, graph, routes):

        routes_costs = [
            self._compute_route_cost(graph, route) for route in routes
        ]

        return routes_costs

    def compute_solution_objective(self, graph, solution):

        routes = self._get_routes(solution)
        routes_costs = self._compute_routes_costs(graph, routes)
        solution_objective = sum(routes_costs)

        return solution_objective

        

def compute_route_weight(graph, route):

    route_edges = solution_utils.get_route_edges(route)
    route_weights = graph_utils.get_edge_weights(graph, route_edges)
    route_weight = sum(route_weights)

    return route_weight

    
