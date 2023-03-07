import collections

from redoute.graph import graph_utils


class _baseClarkeWright():

    def __init__(self, objective_calculator, route_feasibility_checker):

        self._objective_calculator = objective_calculator
        self._route_feasibility_checker = route_feasibility_checker

    def _compute_solution_objective(self, graph, solution):

        solution_objective = self._objective_calculator(graph, solution)

        return solution_objective

    def _check_route_feasibility(self, graph, route):

        is_feasible = self._route_feasibility_checker.check_feasibility(graph, route)

        return is_feasible

    def _setup_initial_routes(self, initial_routes):

        if initial_routes is None:
            initial_routes = self._construct_initial_routes()
        
    def _get_depot_node(self, graph):

        depot_node = graph_utils.get_depot_node(graph)

        return depot_node

    def _get_customer_nodes(self, graph):

        customer_nodes = graph_utils.get_customer_nodes(graph)

        return customer_nodes

    def _construct_single_customer_route(self, depot_node, customer_node):

        single_customer_route = [depot_node, customer_node, depot_node]

        return single_customer_route

    def _construct_single_customer_routes(self, depot_node, customer_nodes):

        constructor = self._construct_single_customer_route
        single_customer_routes = [
            constructor(depot_node, customer_node) for customer_node in customer_nodes
        ]

        return single_customer_routes

    def _construct_initial_routes(self, graph, initial_routes=None):

        depot_node = self._get_depot_node(graph)
        customer_nodes = self._get_customer_nodes(graph)
        
        if initial_routes is None:
            initial_routes = self._construct_single_customer_routes(depot_node, customer_nodes)
            
        return initial_routes

    def _compute_pair_saving(self, graph, first_node, second_node):

        depot_node = self._get_depot_node(graph)
        
        first_edge = [first_node, depot_node]
        second_edge = [depot_node, second_node]
        third_edge = [first_node, second_node]
        
        first_element = self._objective_calculator._compute_route_cost(graph, first_edge)
        second_element = self._objective_calculator._compute_route_cost(graph, second_edge)
        third_element = self._objective_calculator._compute_route_cost(graph, third_edge)

        saving = first_element + second_element - third_element
        
        return saving

    def _get_customer_edges(self, graph):

        depot_node = self._get_depot_node(graph)
        customer_edges = [
            edge for edge in graph.edges if depot_node not in edge
        ]

        return customer_edges
    
    def _construct_savings_list(self, graph):

        customer_edges = self._get_customer_edges(graph)
        savings_list = {
            edge: self._compute_pair_saving(graph, *edge) for edge in customer_edges
        }

        return savings_list

    def _order_savings_list(self, savings_list):

        ordered_savings_list = sorted(savings_list.items(), key=lambda item: item[1])
        savings_list = {
            key: value for (key, value) in reversed(ordered_savings_list)
        }

        return savings_list

    def _get_route_starters(self, routes):

        route_starters = {route[1]: route for route in routes}

        return route_starters
    
    def _get_route_enders(self, routes):

        route_enders = {route[-2]: route for route in routes}

        return route_enders

    def _set_route_starters(self, routes):

        self._route_starters = self._get_route_starters(routes)

        return None

    def _set_route_enders(self, routes):

        self._route_enders = self._get_route_enders(routes)

        return None

    def _merge_routes(self, starter_route, ender_route):

        route = ender_route[:-1] + starter_route[1:]

        return route

    def _get_starter_route(self, second_node):

        starter_route = self._route_starters.get(second_node)

        return starter_route

    def _get_ender_route(self, first_node):

        ender_route = self._route_enders.get(first_node)

        return ender_route

    def _check_route_merge(self, graph, first_node, second_node):

        starter_route = self._get_starter_route(second_node)
        ender_route = self._get_ender_route(first_node)
        if starter_route is None or ender_route is None:
            return None, False
        if first_node in starter_route or second_node in ender_route:
            return None, False
        
        new_route = self._merge_routes(starter_route, ender_route)

        is_feasible = self._check_route_feasibility(graph, new_route)

        return new_route, is_feasible

    def _remove_starter_route(self, second_node):

        if second_node in self._route_starters.keys():
            del(self._route_starters[second_node])

        return None

    def _remove_ender_route(self, first_node):

        if first_node in self._route_enders.keys():
            del(self._route_enders[first_node])
            
        return None

    def _add_starter_route(self, route):

        self._route_starters[route[1]] = route

        return None

    def _add_ender_route(self, route):

        self._route_enders[route[-2]] = route

        return None
        
    def _update_routes(self, graph, first_node, second_node, new_route):

        self._remove_starter_route(second_node)
        self._add_starter_route(new_route)
        starter_node = new_route[-2]
        self._remove_starter_route(starter_node)        
        self._remove_ender_route(first_node)
        self._add_ender_route(new_route)
        ender_node = new_route[1]
        self._remove_ender_route(ender_node)        

        return None

    def _attempt_route_merge(self, graph, first_node, second_node):

        new_route, is_feasible = self._check_route_merge(graph, first_node, second_node)

        if is_feasible:
            self._update_routes(graph, first_node, second_node, new_route)

        return is_feasible

    def _check_saving(self, graph, first_node, second_node):

        if second_node in self._route_starters.keys():
            if first_node in self._route_enders.keys():
                is_feasible = self._attempt_route_merge(graph, first_node, second_node)
                
        return None

    def _check_savings(self, graph):

        for (first_node, second_node), _ in self._savings_list.items():
            self._check_saving(graph, first_node, second_node)

        return None
    
    def _set_initial_routes(self, graph, initial_routes=None):

       routes = self._construct_initial_routes(graph, initial_routes)
       self._set_route_starters(routes)
       self._set_route_enders(routes)

       return None

    def _set_savings_list(self, graph):

        savings_list = self._construct_savings_list(graph)
        self._savings_list = self._order_savings_list(savings_list)

        return None

    def get_routes(self):

        routes = list(self._route_starters.values()) 
        
        return routes

    def get_objective_value(self, graph, routes=None):

        routes = routes or self.get_routes()
        objectve_value = self._objective_calculator.compute_solution_objective(graph, routes) 

        return objectve_value
        
    def solve(self, graph, initial_routes=None, return_objective_value=False):

        clone_graph = graph_utils.clone_graph(graph)
        self._set_initial_routes(clone_graph, initial_routes)
        self._set_savings_list(clone_graph)
        self._check_savings(clone_graph)
        routes = self.get_routes()
        if return_objective_value:
            objective_value = self.get_objective_value(clone_graph)
            return_object = (objective_value, routes)
        else:
            return_object = routes

        return return_object
