"""Provides utility to generate synthetic networks used in initial
experiments. These include scale-free networks with a given exponent,
min, and max degree, as well as LFR benchmarks.

@author Daniel Kaiser. Created on 2022-04-19. Last modified 2022-04-19.
"""
# ===================== IMPORTS =======================
# Standard library
import sys
import os
import random
from typing import Union, List
from itertools import product

## Append path
# sys.path.append(os.path.join("..", "structs/"))

# Scientific computing
import numpy as np

# Network science
import networkx as nx

# Miscelleaneous
from structs.multiplex import Multiplex
from tqdm import tqdm  # ! DEBUG


# ===================== METADATA ======================
__author__ = "Daniel Kaiser"
__credits__ = [
    "Daniel Kaiser",
    "Siddharth Patwardhan",
    "Filippo Radicchi",
]
__version__ = "1.0.0"
__maintainer__ = "Daniel Kaiser"
__email__ = "kaiserd@iu.edu"
__status__ = "Development"


# ===================== FUNCTIONS ==========================
def sample_scalefree_sequence(
    exponent: float, xmin: float, xmax: float,
    n: int = 1, return_ints: bool = False,
    seed: Union[int, None] = None) -> List[Union[float, int]]:
    """Generates a number sequence of length _n_ that approximately fits
    a scale-free distribution with exponent parameter _exponent_ and
    bounds _xmin_, _xmax_.

    NOTE: Scale-free distributions with |exponent| < 2 do not have
    finite variance!

    Parameters
    ----------
    exponent : float
        Scale-free distribution exponent parameter. Must be positive, is
        negated throughout where necessary.
    xmin : float
        Lower bound of sampled sequence.
    xmax : float
        Lower bound of sampled sequence.
    n : int, optional
        Size of sampled sequence, by default 1
    return_ints : bool, optional
        Indicator if returned sequence should consist strictly of ints,
        by default False. NOTE: Truncating to integers may weaken the
        scale-free-ness!
    seed : Union[int, NoneType], optional
        RNG seed for reproducibility, by default None

    Returns
    -------
    List[Union[float, int]]
        Sequence of length _n_ of numbers sampled from a scale-free
        distribution of exponent parameter _exponent_ and bounds
        _xmin_, _xmax_.
    """
    # Book-keeping
    exponent = float(exponent)
    xmin = float(xmin)
    xmax = float(xmax)
    sequence = []

    # Get power terms for sequence min and max
    xm = np.power(xmin, 1-exponent)
    xM = np.power(xmax, 1-exponent)

    # If reproducibility is needed, set seed
    random.seed(seed)

    # Generate n-many sequences fitting the scale-free parameters
    for _ in range(n):
        ## Draw uniformly from [0,1], used to sample from the broader
        ## scale-free sequence
        q = random.random()

        ## Sample from scale-free sequence
        ## Split into two computations for legibility.
        inside = (xM - (xM - xm)*q)
        outside = np.power(inside, np.power(1-exponent, -1))

        # If specified, enforce integer sequence
        # Not necessary for networkx expected degree graphs
        if return_ints:
            outside = int(outside)

        ## Append to sequence
        sequence.append(outside)

    return sequence


def get_expected_degree_graph(
    sequence: List[Union[float, int]], selfloops: bool = True,
    seed: Union[int, None] = None) -> nx.Graph():
    """Generates an undirected, unweighted single-layer network from a
    sequence of expected degrees. This procedure is based on a simple
    stub-matching process and does not create any mesoscale structure
    (except by random chance).

    Parameters
    ----------
    sequence : List[Union[float, int]]
        Expected degree sequence.
    selfloops : bool, optional
        Indicator if self-loops will be allowed in the resultant graph,
        by default True. NOTE: Turning to 'False' may significantly
        alter the actualized degree sequence!
    seed : int, optional
        RNG seed for reproducibility, by default None

    Returns
    -------
    nx.Graph
        Undirected, unweighted networkx Graph object with degree
        sequence approximating input sequence.
    """

    return nx.expected_degree_graph(
        sequence, selfloops=selfloops, seed=seed)


def get_expected_degree_multiplex(
    sequences: List[List[Union[float, int]]], selfloops: bool = True,
    seed: Union[int, None] = None) -> Multiplex:
    """Generates an undirected, unweighted multiplex from a list of
    sequences of expected degrees. This procedure is based on a simple
    stub-matching process and does not create any mesoscale structure
    (except by random chance). Each layer is generated independently of
    the others.

    Parameters
    ----------
    sequences : List[List[Union[float, int]]]
        List of expected degree sequences for each layer.
    selfloops : bool, optional
        Indicator if self-loops will be allowed in the resultant
        multiplex layers, by default True. NOTE: Turning to 'False' may
        significantly alter the actualized degree sequence!
    seed : int, optional
        RNG seed for reproducibility, by default None

    Returns
    -------
    Multiplex
        Undirected, unweighted custom class containing nx.Graph objects
        with degree sequence approximating input sequences.
    """

    multiplex = {}
    for idx, sequence in enumerate(sequences):
        multiplex[idx] = get_expected_degree_graph(
            sequence=sequence, selfloops=selfloops, seed=seed
        ).edges

    return Multiplex(multiplex_dict=multiplex)


def generate_variable_redundant_duplex(
    graph: nx.Graph, redundancy: float = 1.0) -> Multiplex:
    """Generates a duplex with a given redundancy (overlap) to a given
    single-layer network.

    NOTE: Does not necessarily preserve degree distribution or mesoscale
    structures!

    Parameters
    ----------
    graph : nx.Graph
        Single-layer network. The returned duplex will have this as one
        layer, and some generated layer with specified redundancy as the
        other layer.
    redundancy : float, optional
        Fraction of edge overlap between the two layers, by default 1.0.
        Must be in [0,1]

    Returns
    -------
    Multiplex
        Two-layer Multiplex class object with layer 0 the given single-
        layer network, and layer 1 being the layer generated with
        specified redundancy.
    """

    # Instantiate multiplex adjacency list
    multiplex = {0: list(graph.edges)}

    # Generate new layer with specified redundancy
    ## Insantiate empty graph with same node set
    redundant_graph = nx.Graph()
    redundant_graph.add_nodes_from(graph.nodes)

    ## Select random chunk of edges to be redundant and add to graph
    cutoff_count = int(redundancy*len(multiplex[0]))
    redundant_graph.add_edges_from(
        random.sample(multiplex[0], k=cutoff_count)
    )

    ## Add more edges to maintain _m_, avoiding more redundancy
    ## NOTE: Does not preserve degree distribution!
    elligible_remaining_edges = \
        set(product(tuple(graph.nodes), tuple(graph.nodes)))
    elligible_remaining_edges = elligible_remaining_edges - \
            set(graph.edges).union(set(redundant_graph.edges))
    redundant_graph.add_edges_from(
        random.sample(
            elligible_remaining_edges,
            k=len(multiplex[0])-cutoff_count
        )
    )

    # Add to multiplex adjacency list
    multiplex[1] = list(redundant_graph.edges)

    return Multiplex(multiplex_dict=multiplex)



# ============================ MAIN ====================================
if __name__ == "__main__":
    # Gen initial layer
    ## Get degree sequence
    graph_ = sample_scalefree_sequence(
        exponent=2.5, xmin=3, xmax=np.sqrt(1000),  # Distribution params
        n=1000,  # Size of sample
        seed=37  # Reproducible seed
    )

    ## Get expected degree stub-matching graph
    graph = get_expected_degree_graph(graph_, seed=37)

    # Generate handful of multiplexes
    for red in tqdm(np.linspace(0,1,100,True)):
        multiplex = generate_variable_redundant_duplex(graph, red)
        multiplex.save_edgelist(f"data/redundant_benchmarks/redundant_duplex_red-{red:.3f}.edgelist")