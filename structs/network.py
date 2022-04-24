"""Provides Network.
"""

# ===================== IMPORTS =======================
# Standard library
import sys
from itertools import combinations
from typing import List

# Scientific computing
import pandas as pd
import numpy as np
from scipy.stats import spearmanr as sp
from scipy.stats import pearsonr as pr

# Network science
import networkx as nx
from cdlib.algorithms import louvain
from cdlib.evaluation import newman_girvan_modularity as modularity

# Miscelleaneous
from structs.core import MultiplexCore


# ===================== METADATA ======================
__author__ = "Daniel Kaiser"
__credits__ = [
    "Daniel Kaiser",
    "Siddharth Patwardhan",
    "Filippo Radicchi",
    "Stephen Jasina",
]
__version__ = "1.1.1"
__maintainer__ = "Daniel Kaiser"
__email__ = "kaiserd@iu.edu"
__status__ = "Development"


# ===================== CLASS ==========================
class Multiplex(MultiplexCore):
    """Class to handle Multiplex data in the context of reconstruction
    experiments."""
    # ~~~ Init and data retrieval ~~~
    def __init__(self, multiplex_dict=None):
        super().__init__(multiplex_dict)
        self.layer_pairs = \
            list(combinations(range(self.number_of_layers), 2))

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
    def get_entropy(self):
        pass