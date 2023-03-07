from redoute.graph import graph_utils
from redoute.graph import problem_utils


class feasibilityChecker():

    def __init__(self, feasibility_checkers):

        self._feasibility_checkers = feasibility_checkers


    def _check_feasibility(self, graph, route, feasibility_checker):

        is_feasible = feasibility_checker(graph, route)

        return is_feasible

    def check_feasibility(self, graph, route):

        is_feasible = all([
            self._check_feasibility(graph, route, feasibility_checker)
            for feasibility_checker in self._feasibility_checkers
        ])

        return is_feasible


def check_capacity_feasibility(graph, route):

    vehicle_capacity = problem_utils.get_vehicle_capacity(graph)
    node_demands = problem_utils.get_node_demands(graph, route)
    is_feasible = sum(node_demands) <= vehicle_capacity

    return is_feasible
