import numpy as np

from redoute.graph import graph_utils


class feasifierWrapper():

    def feasify_prune_vector(self, graph, y):
        """ Given the pruning vector, feasify it """

        feasified_vector = (self.compute_feasifier_vector(graph) + y).astype(bool) 
        
        return feasified_vector


class blankFeasifier(feasifierWrapper):

    def compute_feasifier_vector(self, graph):
        """ Compute the feasifier vector """

        feasifier_vector = np.ones((len(graph.edges))) 
        
        return feasifier_vector
    

class scratchFeasifier(feasifierWrapper):

    def __init__(self, stuff=None):

        self.stuff = None

    def _compute_nonzeros(self, graph):
        """ Compute the number of indices that should be nonzero """
        
        number_of_nonzeros = len(graph.nodes) /  len(graph.edges)

        return number_of_nonzeros

    def _fudge_feasifier_vector(self, graph):
        """ Compute a fudged feasifier vector """

        p = _compute_nonzeros(self, graph)
        feasifier_vector = np.random.choice([0, 1], size=(m), p=[1-p, p]) 
        
        return feasifier_vector

    def compute_feasifier_vector(self, graph):
        """ Compute the feasifier vector """

        feasifier_vector = self._fudge_feasifier_vector(graph)
        
        return feasifer_vector

    
_feasifiers = [
    None,
    scratchFeasifier,
]
