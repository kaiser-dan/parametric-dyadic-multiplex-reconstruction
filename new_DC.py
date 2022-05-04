"""THING

@ author Daniel Kaiser. Created on 2022-01-26 09:52:00 EST.
"""
# ====================== IMPORTS AND GLOBALS ==================
# Standard library
import sys
from enum import Enum, unique, auto
from typing import Dict, Tuple, Union, List

# Scientific computing
import numpy as np

# Network science
import networkx as nx
from cdlib.algorithms import louvain

# Miscellaneous

# ===================== METADATA ======================
__author__ = "Daniel Kaiser"
__credits__ = ["Daniel Kaiser", "Siddharth Patwardhan", "Filippo Radicchi"]
__version__ = "2.1.2"
__maintainer__ = "Daniel Kaiser"
__email__ = "kaiserd@iu.edu"
__status__ = "Development"

# ========================== FUNCTIONS ========================
# ------ Helpers and Constants -------
@unique
class Method(Enum):
    DEGREE = 0
    COMMUNITY = auto()
    DEGREECOMMUNITY = auto()

    def __str__(self):
        return self.name.lower().capitalize()

def _process_reconstruction(reconstruction, observed_layers):

def _classify_edge(edge, remnant_degrees: Dict[List[int]], remnant_communities):
    return  # ! CALLS EDGE LIKELIHOOD

# ------ Calculation helpers -------
def _edge_likelihood():
    return

def _thing():


# ------- Drivers -------
def reconstruct(
    aggregate: List[Tuple[int]], observed_layers: Dict[List[int]], degrees,
        method) -> Dict[List[Tuple[int]]]:
    # ! ASSUMED TO BE VALID INPUT
    # Book-keeping
    _observed_layers = \
        {
            key: set(value) for key, value in observed_layers.items()
        }  # * Converting to set edgelists to help with _aggregate
    _aggregate = \
        set(aggregate).difference(
            set().union(*list(_observed_layers.values()))
        )  # * Aggregate edges with no a priori information ("to-classify")

    # Form remnants
    remnant_layers = get_remnants(aggregate, observed_layers)

    # Get information from remnants used in reconstruction
    remnant_degrees = get_remnant_degrees(remnant_layers)
    remnant_communities = get_remnant_communities(remnant_layers)  # ! MAYBE NEED MU RETURNED HERE TOO?

    # Do reconstruction
    reconstruction = \
        {
            edge: _classify_edge(edge, STUFF)
        }

    return