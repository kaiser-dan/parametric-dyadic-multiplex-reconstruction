"""Provides Multiplex, class to store and manipulate multiplex network data.

Multiplex must be instantiated with a relative filepath to a
multiplex edgelist. Each line of this file should report a new edge,
formatted as [LAYER] [NODE] [NODE]. Multiplex provides a method for
saving to this format as well, should any changes be made to the topology.

This class was originally prepared for research. The class here
represents a more polished, documented form of what was used to
do the research, however, is functionally equivalent. Metadata,
then, does not reflect research timeline.

@author Daniel Kaiser. Created on 2022-04-10. Last modified 2022-04-14.
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
    def get_degree_sequences(self, all_nodes: bool = False):
        # Get degree sequence in each layer
        ## If forcing common node set, initialize empty degree sequences
        if all_nodes:
            degrees = [
                [0]*(self.total_number_of_nodes+1)
                for _ in range(self.number_of_layers)
            ]

            ## Update degree sequences with active node degrees
            for layer_idx, layer in enumerate(self.multiplex):
                degrees_ = list(layer.degree())
                for c, degree in enumerate(degrees_):
                    #degrees[layer_idx][degree[0]] = degree[1]
                    degrees[layer_idx][c] = degree[1]

        ## If only considering active nodes, retrieve degrees
        else:
            degrees = [list(dict(layer.degree()).values()) for layer in self.multiplex]

        return degrees

    def get_degree_correlation(self, correlation_measure: str = "PEARSON"):
        # Validate parameters
        correlation_measure = correlation_measure.upper()
        if correlation_measure not in ["PEARSON", "SPEARMAN"]:
            raise NotImplementedError(f"{correlation_measure} is not a supported correlation measure!")

        # Get pairwise degree sequence correlations
        correlations = {}

        ## Get total degree sequences
        ## If not already calculated, get them!
        if not hasattr(self, "total_degree_sequences"):
            self.total_degree_sequences = self.get_degree_sequences(True)
        for layer_pair in self.layer_pairs:
            ## If selected, run each potential pairwise degree correlation
            if correlation_measure == "PEARSON":
                correlations[layer_pair] = \
                    pr(
                        self.total_degree_sequences[layer_pair[0]],
                        self.total_degree_sequences[layer_pair[1]]
                    )[0]
            else:
                correlations[layer_pair] = \
                    sp(
                        self.total_degree_sequences[layer_pair[0]],
                        self.total_degree_sequences[layer_pair[1]]
                    )[0]

        return correlations

    def get_node_overlap(self):
        overlap = {}
        for layer_pair in self.layer_pairs:
            nodes_left = set(self.multiplex[layer_pair[0]].nodes)
            nodes_right = set(self.multiplex[layer_pair[1]].nodes)
            jaccardian = len(nodes_left & nodes_right) / len(nodes_left | nodes_right)
            overlap[layer_pair] = jaccardian

        return overlap

    def get_edge_overlap(self):
        overlap = {}
        for layer_pair in self.layer_pairs:
            nodes_left = set(self.multiplex[layer_pair[0]].nodes)
            nodes_right = set(self.multiplex[layer_pair[1]].nodes)
            jaccardian = len(nodes_left & nodes_right) / len(nodes_left | nodes_right)
            overlap[layer_pair] = jaccardian

        return overlap

    def get_average_degree_ratios(self):
        ratios = {}
        for layer_pair in self.layer_pairs:
            average_left = np.mean(
                list(dict(self.multiplex[layer_pair[0]].degree()).values())
            )
            average_right = np.mean(
                list(dict(self.multiplex[layer_pair[1]].degree()).values())
            )
            averages = [average_left, average_right]
            ratios[layer_pair] = min(averages) / max(averages)

        return ratios

    def get_modularities(self):
        modularities = [
            max([
                x for x in modularity(graph,louvain(graph))
                if x is not None
            ])
            for graph in self.multiplex
        ]
        return modularities

    def get_nmis(self):
        nmis = {}
        for layer_pair in self.layer_pairs:
            left = nx.Graph()
            right = nx.Graph()

            left_ = self.multiplex[layer_pair[0]]
            right_ = self.multiplex[layer_pair[1]]

            common_node_set = tuple(set(left_.nodes) | set(right_.nodes))
            left.add_nodes_from(common_node_set)
            right.add_nodes_from(common_node_set)

            left.add_edges_from(left_.edges)
            right.add_edges_from(right_.edges)

            left_communities = louvain(left)
            right_communities = louvain(right)

            nmi = max([
                x for x in left_communities.normalized_mutual_information(right_communities)
                if x is not None
            ])

            nmis[layer_pair] = nmi


        return nmis

    def summarize_multiplex_layers(self):
        if not hasattr(self, "modularities"):
            self.modularities = self.get_modularities()

        df = pd.DataFrame({
            "Layer": range(1, self.number_of_layers+1),
            "ActiveNodeCount": self.number_of_nodes,
            "ActiveEdgesCount": self.number_of_edges,
            "ComponentsCount": self.number_of_components,
            "Modularity": self.modularities,
        })

        return df

    def summarize_multiplex_pairs(self):
        if not hasattr(self, "node_overlap"):
            self.node_overlap = self.get_node_overlap()
        if not hasattr(self, "edge_overlap"):
            self.edge_overlap = self.get_edge_overlap()
        if not hasattr(self, "average_degree_ratios"):
            self.average_degree_ratios = self.get_average_degree_ratios()
        if not hasattr(self, "degree_correlations"):
            self.degree_correlations = self.get_degree_correlation("PEARSON")
        if not hasattr(self, "nmis"):
            self.nmis = self.get_nmis()

        lefts, rights = list(zip(*self.layer_pairs))
        df = pd.DataFrame({
            "LayerLeft": lefts,
            "LayerRight": rights,
            "NodeOverlap": self.node_overlap.values(),
            "EdgeOverlap": self.edge_overlap.values(),
            "AverageDegreeRatio": self.average_degree_ratios.values(),
            "DegreeSequenceCorrelation": self.degree_correlations.values(),
            "NMI": self.nmis.values(),
        })

        return df


    # ~~~ Public methods to aggregate ~~~
    def aggregate_multiplex(self, aggregation_mechanism: str):
        # Homoegenize casing to parse
        aggregation_mechanism = aggregation_mechanism.upper()

        # Gather sets of each edgelist
        layers_ = list(self._multiplex_dict.values())

        # Apply set operation corresponding to specified aggregation
        if aggregation_mechanism == "OR":
            aggregate_ = set().union(*layers_)
        elif aggregation_mechanism == "AND":
            aggregate_ = set().intersection(*layers_)
        elif aggregation_mechanism == "XOR":
            aggregate_ = set().union(*layers_) - set().intersection(*layers_)
        else:
            ## Check implementation support for specified mechanism
            return \
                NotImplementedError(
                    "{} not a supported aggregation mechanism"
                    .format(aggregation_mechanism)
                    )

        return nx.Graph(aggregate_), aggregation_mechanism


class MultiplexCorpus:
    def __init__(self, multiplexes: List[Multiplex]):
        self.corpus = multiplexes

    def summarize_corpus(self):
        # ADD ALL THIS STUFF TO TABLES AND CONCATENATE
        return