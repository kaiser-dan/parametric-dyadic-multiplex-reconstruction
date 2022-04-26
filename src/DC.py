""" Script handling community detection portion of Robustness Modularity project experiments.
Note that this script is still in development!

@ author Daniel Kaiser. Created on 2022-01-26 09:52:00 EST.
"""
# ====================== IMPORTS AND GLOBALS ==================
# Standard library
import sys
import random
from itertools import starmap

# Scientific computing
import numpy as np

# Network science
import networkx as nx
from cdlib.algorithms import louvain
from sympy import numer

# Custom
sys.path.append("..")
from structs.multiplex import Multiplex
from structs.core import read_edgelist


# ========================== FUNCTIONS ========================
# -------- Helpers --------
# ~~~ Processing ~~~
## ~ Input processing ~
def process_degrees(additional_information_fh):
    # Open file and extract raw data
    with open(additional_information_fh) as fh_:
        degree_sequences_ = fh_.readlines()

    # Initialize empty array of degree sequences
    degree_sequences = []

    # Add each layer's degree sequence to total array
    for layer in degree_sequences_:
        # Split string into list of degrees per node
        layer = [degseq.rstrip().split(" ") for degseq in degree_sequences_]

        # Convert type
        layer = list(map(int, layer))

        # Add to total array
        degree_sequences.append(layer)

    return degree_sequences

def process_observations(_aggregate_edges, additional_information_fh):
    # * NOTE: Observed multiplex must be of the form "[LAYER] [SRC] [TGT]" where the edge ([SRC], [TGT]) is in the aggregate!
    _observed_multiplex_dict = read_edgelist(additional_information_fh, "MULTIPLEX", "STANDARD")  # Multiplex edgelist for known edges
    if not 0 in _observed_multiplex_dict:
        _observed_multiplex_dict[0] = []
    if not 1 in _observed_multiplex_dict:
        _observed_multiplex_dict[1] = []
    _estimated_multiplex = Multiplex(multiplex_dict={
        layer: _aggregate_edges.difference(set(edgelist))
        for layer, edgelist in _observed_multiplex_dict.items()
    })

    return _observed_multiplex_dict, _estimated_multiplex

## ~ Output processing ~
def process_reconstruction(reconstruction_mapping_, _observed_multiplex_dict = None):
    reconstruction_dict_ = {}
    for edge, layer in reconstruction_mapping_.items():
        if layer not in reconstruction_dict_:
            reconstruction_dict_[layer] = {edge}
        else:
            reconstruction_dict_[layer].add(edge)

    if _observed_multiplex_dict is not None:
        ## Add partial observations back to layer edgelist mapping
        # * NOTE: In observation processing, correct number of layers is added!
        for layer, edges in _observed_multiplex_dict.items():
            reconstruction_dict_[layer].union(edges)

    ## Instantiate the class object and return
    return  Multiplex(multiplex_dict=reconstruction_dict_)


# ~~~ Reconstruction calculations ~~~
## ~ Low-level calculations ~
def edge_assignment_probability(edge, layer_idx, degree_sequences, partitions = None, mu = 1.0):
    src, tgt = edge

    # Set probability weights
    ## If partitions don't match, or there are no partitions, set trivial weights
    weights = [1 for _ in partitions]

    ## If partitions available, use community strength to inform weights
    if partitions is not None:
        ## Calculate weight by community strength when incidence node's communities align
        if all(src in partition for partition in partitions) and all(tgt in partition for partition in partitions):
            delta = lambda partition_src, partition_tgt, mu: mu if partition_src == partition_tgt else 1-mu
            weights = [
                delta(partition[src], partition[tgt], mu)
                for partition in partitions
            ]

    # Calculate likelihood edge originates from layer_idx
    # * Assumes a configuration model likelihood of edge placement within each layer
    try:
        numerator = weights[layer_idx] * \
            degree_sequences[layer_idx][src] * \
            degree_sequences[layer_idx][tgt]
        denominator = np.sum([
            weights[idx_] * \
                degree_sequences[idx_][src] * \
                degree_sequences[idx_][tgt]
            for idx_ in range(len(degree_sequences))
        ])
    except IndexError:
        numerator = 0
        denominator = 1

    return numerator / denominator

def estimate_mu(_estimated_multiplex):
    ### Retrieve estimate partitions
    estimated_multiplex_partitions = [
        louvain(estimated_layer.graph).to_node_community_map()
        for estimated_layer in _estimated_multiplex.multiplex
    ]

    ### Estimate community strength
    pin,pout=0,0
    estimated_mus = []
    for idx, estimated_layer in enumerate(_estimated_multiplex.multiplex):
        #### Check that there is an estimated layer
        #### If completely observed, will cause ZeroDivisionError
        if len(estimated_layer.graph.edges) == 0:
            estimated_mus.append(0)
        else:
            #### Get tuples of partition assignments for end of edges
            #### [ (partition of edge source, partition of edge target) for edges ]
            edge_ends_communities = []
            for edge in estimated_layer.graph.edges:
                edge_ends_communities.append((
                    estimated_multiplex_partitions[idx][edge[0]][0],
                    estimated_multiplex_partitions[idx][edge[1]][0]
                ))
            grouped_ = zip(*edge_ends_communities)

            #### Restrict to edges where both ends belong to same community
            grouped = {
                edge_partition
                for edge_partition in grouped_
                if edge_partition[0] == edge_partition[1]
            }

            #### Estimate community strength as relative size of this restriction
            mu_ = len(grouped) / estimated_layer.number_of_edges
            estimated_mus.append(mu_)

    ### Take weighted average of community strengths across layers
    ### Weight by size of *known* topology in that layer
    known_sizes = _estimated_multiplex.number_of_edges
    try:
        mu = sum(
                [estimated_mus[idx] * known_sizes[idx] for idx in range(len(known_sizes))]
            ) / sum(known_sizes)
    except:  # ! NEED TO CATCH SAFELY
        #raise ValueError("No partial information, division by 0 in estimating mu!")
        mu = 0.5
    finally:
        return mu, estimated_multiplex_partitions

## ~ High-level calculations ~
def get_reconstruction_mapping(_aggregate_edges, _observed_multiplex_dict, _degree_sequences, _estimated_multiplex_partitions, mu):
    # Simplify reconstruction input edge set
    _edges_to_classify = _aggregate_edges.difference(set().union(*_observed_multiplex_dict.values()))

    # Initialize trivial reconstruction mapping
    reconstruction_mapping_ = {edge: 0 for edge in _edges_to_classify}

    # Fill in reconstructed layer assignments according to likelihood
    for edge in reconstruction_mapping_:
        ## Probability of assignment to each layer
        probs_ = [
            edge_assignment_probability(edge, idx, _degree_sequences, _estimated_multiplex_partitions, mu)
            for idx in _observed_multiplex_dict
        ]

        ## Selecting layer to which edge most likely belongs
        ## * NOTE: Doing hard choice now, can do proportionally if desired
        assignment_ = np.random.choice(
            np.flatnonzero(probs_ == np.max(probs_))
        )

        ## Update mapping
        reconstruction_mapping_[edge] = assignment_

    return reconstruction_mapping_


# ------ Main algorithms ------
def reconstruct_from_aggregate_via_observations(aggregate: nx.Graph(), additional_information_fh, use_community_detection=True):
    """THING

    NOTE: All validation is done externally and prior to application of this function!
    """
    # Book-keeping
    ## Process aggregate network
    _aggregate_edges = set(aggregate.edges)  # Set of edges in the aggregate

    ## Process observation data
    _observed_multiplex_dict, _estimated_multiplex = process_observations(_aggregate_edges, additional_information_fh)

    # Apply and utilize community detection
    if use_community_detection:
        mu, _estimated_multiplex_partitions = estimate_mu(_estimated_multiplex)
    else:
        mu, _estimated_multiplex_partitions = 1.0, None # Dummy value, does not preclude/indicate community structure

    # Apply reconstruction
    _degree_sequences = _estimated_multiplex.get_degree_sequences(all_nodes=True)
    reconstruction_mapping_ = get_reconstruction_mapping(_aggregate_edges, _observed_multiplex_dict, _degree_sequences, _estimated_multiplex_partitions, mu)

    # Process reconstruction mapping
    reconstruction_multiplex = process_reconstruction(reconstruction_mapping_, _observed_multiplex_dict)

    # Return reconstructed multiplex
    return reconstruction_multiplex


def reconstruct_from_aggregate_via_degrees(aggregate: nx.Graph(), additional_information_fh):
    """THING
    """
    # Book-keeping
    ## Process aggregate network
    _aggregate_edges = set(aggregate.edges)  # Set of edges in the aggregate

    ## Process degree sequence data
    # _observed_multiplex_dict, _estimated_multiplex_graphs = process_observations(_aggregate_edges, additional_information_fh)
    layer_degree_sequences = process_degrees(additional_information_fh)

    # Dummy values for community element to fit functional form
    mu, _estimated_multiplex_partitions = 1.0, None # Dummy value, does not preclude/indicate community structure

    # Apply reconstruction
    _observed_multiplex_dict = {}  # Dummy value to maintain get_reconstruction_mapping formatting!
    reconstruction_mapping_ = get_reconstruction_mapping(_aggregate_edges, _observed_multiplex_dict, layer_degree_sequences, _estimated_multiplex_partitions, mu)

    # Process reconstruction mapping
    reconstruction_multiplex = process_reconstruction(reconstruction_mapping_)

    # Return reconstructed multiplex
    return reconstruction_multiplex