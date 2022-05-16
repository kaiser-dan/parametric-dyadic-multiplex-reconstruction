"""
@author Daniel Kaiser. Created on 2022-05-05.
"""
# ===================== IMPORTS =======================
# Standard library
import random
from itertools import chain

# Scientific computing
import numpy as np

# Network science
import networkx as nx
from cdlib.algorithms import louvain

# Custom modules

# Miscelleaneous
## Imports

## Aliases


# ===================== METADATA ======================
__author__ = ["Daniel Kaiser", "Siddharth Patwardhan"]
__credits__ = ["Daniel Kaiser", "Siddharth Patwardhan", "Filippo Radicchi"]
__version__ = "3.2.0"
__maintainer__ = "Daniel Kaiser"
__email__ = "kaiserd@iu.edu"
__status__ = "Development"

# ==================== FUNCTIONS =======================
# ------------- I/O processing -------------
def process_partial_observations(aggregate, observed_layers):
    pass

def process_edge_classifications(classifications):
    pass


# ---------- Calculation helpers -----------
def calculate_edge_likelihoods(edge, degrees, mu=0.5, partitions=None):
    # Book-keeping
    src = edge[0]
    tgt = edge[1]

    degree_products = {
        layer_idx: degrees[layer_idx][src]*degrees[layer_idx][tgt]
        for layer_idx in degrees
        }

    adj_mu = \
        lambda src_partition, tgt_partition, mu: mu if src_partition == tgt_partition else 1-mu
    denominator = sum(degree_products.values())
    likelihoods = {
        layer_idx: \
            adj_mu(partitions[layer_idx][src], partitions[layer_idx][tgt], mu) \
            * (degree_products[layer_idx] / denominator)
        for layer_idx in degree_products
    }

    return likelihoods

def get_partitions(remnants):
    # Calculate partitions of remnants
    partitions = {
        layer_idx: louvain(remnant).to_node_community_map()
        for layer_idx, remnant in remnants.items()
    }
    ### * Need to adjust for cdlib output returning a list of community assignments!
    for layer_idx, mapping in partitions.items():
        partitions[layer_idx] = mapping[0]

    # Calculate community strength, mu
    p_ins = {layer_idx: 0 for layer_idx in remnants}
    p_outs = {layer_idx: 0 for layer_idx in remnants}

    # Calculate probability of internal and external edges to groups
    for idx, remnant in remnants.items():
        edge_incident_communities = \
            np.array([
                [partitions[layer_idx][edge[0]] for edge in remnant.edges],
                [partitions[layer_idx][edge[1]] for edge in remnant.edges]
            ])

        p_ins[layer_idx] = \
            np.count_nonzero(np.array(edge_incident_communities[0] == edge_incident_communities[1], dtype=int))
        p_outs[layer_idx] = len(remnant.edges)

    # Calculate communtiy strength
    try:
        mu = sum(p_ins.values()) / (sum(p_ins.values()) + sum(p_outs.values()))
    except ZeroDivisionError:
        mu = 0.5

    return partitions, mu


# ----------------- Drivers ----------------
def reconstruct_from_observations(aggregate, observations: dict = None,
        use_community_detection: bool = False, soft_classifications: bool = False):
    # Book-keeping
    reconstruction_mapping = {}

    # Form remnants
    # * Used to inform likelihood calculations
    ## Form edgelists
    remnants_ = {
        layer_idx: set(aggregate) - set(observed_layer) for layer_idx, observed_layer in observations.values()
    }

    ## Get all nodes
    ## * Avoids missing node indices!
    remnant_nodes = set.union(*[list(chain(*rem)) for rem in remnants_])

    ## Form nx.Graph objects and track degree sequences
    remnants = {}
    degrees = {}
    for layer_idx in remnants_:
        ### Initialize graph
        graph_ = nx.Graph()

        ### Add nodes (even if under XOR they may be isolated in some layer)
        graph_.add_nodes_from(remnant_nodes)

        ### Add remnant edges
        graph_.add_edges_from(remnants_[layer_idx])

        ### Update graph object
        remnants[layer_idx] = graph_

        ### Track degree sequences for likelihood calculations
        degrees[layer_idx] = graph_.degree()

    # Start reconstruction body
    ## Calculate communities, if applicable
    if use_community_detection:
        partitions, mu = get_partitions(remnants)
    else:
        partitions, mu = None, 0.5  # Dummy values for likelihood if communities not utilized

    ## Loop over unclassified edges
    unknown_aggregate_edges = \
        set(aggregate).difference(
            set.union(*[edges for edges in observations.values()])
        )
    for edge in unknown_aggregate_edges:
        ### Calculate likelihood of edge belonging to each layer
        likelihoods = calculate_edge_likelihoods(edge, degrees, mu, partitions)

        ### Hard classification - take most likely layer
        reconstruction_mapping[edge] = max(likelihoods, key=likelihoods.get)

    return reconstruction_mapping