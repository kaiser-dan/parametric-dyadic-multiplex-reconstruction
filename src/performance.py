"""Provides utility to analyze how similar one multiplex
structure is from another. Implicitly assumes one structure is a
reconstructed multiplex, and the other is ground-truth. Hence, this
allows the comparison to be throught of as reconstruction performance or
accuracy.

@author Daniel Kaiser. Created on 2022-04-19. Last modified 2022-04-19.
"""
# ===================== IMPORTS =======================
# Standard library
import sys

# Scientific computing
import numpy as np
from sklearn.metrics import auc

# Network science
import networkx as nx

# Miscelleaneous
sys.path.append("..")
from structs.multiplex import Multiplex


# ===================== METADATA ======================
__author__ = "Daniel Kaiser"
__credits__ = [
    "Daniel Kaiser",
    "Siddharth Patwardhan",
]
__version__ = "1.0.0"
__maintainer__ = "Daniel Kaiser"
__email__ = "kaiserd@iu.edu"
__status__ = "Development"


# ===================== FUNCTION ==========================
def get_accuracy(aggregate: nx.Graph, reconstructed: Multiplex, original: Multiplex):
    edges_ = aggregate.edges
    correctly_reconstructed = []
    incorrectly_reconstructed = []

    for edge in edges_:
        reconstructed_layers_with_edge = [
            layer
            for layer, graph in enumerate(reconstructed.multiplex) if edge in graph.edges
        ]
        original_layers_with_edge = [
            layer
            for layer, graph in enumerate(original.multiplex) if edge in graph.edges
        ]

        if sorted(reconstructed_layers_with_edge) == sorted(original_layers_with_edge):
            correctly_reconstructed.append(edge)
        else:
            incorrectly_reconstructed.append(edge)

    return len(correctly_reconstructed) / \
        (len(correctly_reconstructed) + len(incorrectly_reconstructed))

def get_correct_layer_subgraphs(reconstructed, original):
    # RETURNS THE MULTIPLEX WHERE EACH LAYER IS ONLY THE SUBSET OF
    # THE CORRESPONDING LAYER OF RECONSTRUCTED THAT IS CORRECTLY PLACED
    # IN THAT LAYER. NOTE, THIS DOES NOT HAVE FEATURES CURRENTLY TO
    # ACCOUNT FOR CORRECT RECONSTRUCTION BUT MISORDERED
    return

def get_auc(x_coords, y_coords):
    return auc(x_coords, y_coords)