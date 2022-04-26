"""Provides Network.
"""

# ===================== IMPORTS =======================
# Standard library
from typing import List

# Scientific computing

# Network science
from cdlib.algorithms import louvain
from cdlib.evaluation import newman_girvan_modularity as modularity

# Miscelleaneous
from structs.core import NetworkCore


# ===================== METADATA ======================
__author__ = "Daniel Kaiser"
__credits__ = [
    "Daniel Kaiser",
    "Siddharth Patwardhan",
    "Filippo Radicchi",
    "Stephen Jasina",
]
__version__ = "1.0.3"
__maintainer__ = "Daniel Kaiser"
__email__ = "kaiserd@iu.edu"
__status__ = "Development"


# ===================== CLASS ==========================
class Network(NetworkCore):
    """Class to handle Multiplex data in the context of reconstruction
    experiments."""
    # ~~~ Init and data retrieval ~~~
    def __init__(self, edgelist=None):
        super().__init__()

    # ~~~ Representations and statics ~~~
    def __repr__(self):
        return "Multiplex(multiplex_dict{!r})".format(self._multiplex_dict)

    def __eq__(self, other):
        if not isinstance(other, Multiplex):
            return NotImplemented

        if self._multiplex_dict.keys() != other._multiplex_dict.keys():
            return False

        for idx_ in self._multiplex_dict:
            if self._multiplex_dict[idx_] != other._multiplex_dict[idx_]:
                return False

        return True

    # ~~~ Public methods to measure structural indicators ~~~
    def get_degrees(self):
        return [deg for _, deg in self.graph.degree()]

    def get_modularity(self):
        return modularity(self.graph, louvain(self.graph))

    def get_entropy(self):
        pass