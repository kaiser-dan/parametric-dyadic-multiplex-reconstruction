"""UPDATE

@author Daniel Kaiser. Created on 2022-04-10. Last modified 2022-04-14.
"""
# ===================== IMPORTS =======================
# Standard library
from multiprocessing.sharedctypes import Value
import pickle

# Scientific computing
import numpy as np

# Network science
import networkx as nx

# Miscelleaneous
from tabulate import tabulate


# ===================== METADATA ======================
__author__ = "Daniel Kaiser"
__credits__ = [
    "Daniel Kaiser",
    "Siddharth Patwardhan",
    "Filippo Radicchi",
    "Stephen Jasina",
    "JT Underhill",
    "Emma Delph",
]
__version__ = "1.4.3"
__maintainer__ = "Daniel Kaiser"
__email__ = "kaiserd@iu.edu"
__status__ = "Development"


# ===================== CLASS ==========================
class NetworkCore:
    """Class to handle single-layer network data."""
    def __init__(self, edgelist=None):
        if edgelist is None:
            raise ValueError("You gotta give me somethin, bro")

        self.graph = nx.Graph(edgelist, nodetype=int)
        self.n = self.graph.number_of_nodes()
        self.m = self.graph.number_of_edges()

    def save_edgelist(self, output_filepath: str):
        nx.write_edgelist(self.graph, output_filepath)

        return f"Graph saved to file {output_filepath}"

    @classmethod
    def save_pickle(self, output_filepath: str):
        # NOTE: This is not necessarily a safe option!
        with open(output_filepath, "wb") as fh_:
            pickle.dump(self, fh_, pickle.HIGHEST_PROTOCOL)

        return f"Multiplex class instance pickled at {output_filepath}"

    def get_adjacency(self):
        return nx.to_numpy_matrix(self)


class MultiplexCore:
    """Class to handle multiplex data."""
    # ~~~ Init and data retrieval ~~~
    def __init__(self, multiplex_dict = None):
        if multiplex_dict is None:
            raise ValueError("You gotta give me somethin, bro")

        # Base representations
        self._multiplex_dict = multiplex_dict
        self.multiplex = [
            NetworkCore(edgelist)
            for edgelist in self._multiplex_dict.values()
        ]  # Networkx graph objects for each layer (ordered)

        # Topological object counts
        self.number_of_layers = len(self._multiplex_dict)
        self.number_of_nodes, self.number_of_edges, self.node_counts, \
            self.edge_counts = self.get_node_edge_counts()

        # Topological connectedness
        self.component_counts = \
            [
                nx.number_connected_components(layer.graph)
                for layer in self.multiplex
            ]

        # Alternative representations
        self.aggregate = None, None  # Aggregated network (topology, type)
        self.supraadjacency = None  # Supra-adjacency matrix

    def save_edgelist(self, output_filepath: str):
        edges = set()
        for layer, edges_ in self._multiplex_dict.items():
            for edge in edges_:
                edges.add("{} {} {}\n".format(layer, edge[0], edge[1]))

        with open(output_filepath, "w") as fh_:
            fh_.writelines(edges)

        print("Multiplex edgelist written at {}".format(output_filepath))

        return

    @classmethod
    def save_pickle(self, output_filepath: str):
        with open(output_filepath, "wb") as fh_:
            pickle.dump(self, fh_, pickle.HIGHEST_PROTOCOL)

        print("Multiplex class instance pickled at {}".format(output_filepath))

        return

    # ~~~ Representations and statics ~~~
    def __repr__(self):
        return "MultiplexCore(multiplex_dict{!r})".format(self._multiplex_dict)

    def __str__(self):
        len_ = len(self._multiplex_dict)
        str_ = {
            "Total unique nodes": [self.total_number_of_nodes] + [""]*(len_-1),
            "Total unique edges": [self.total_number_of_edges] + [""]*(len_-1),
            "Number of layers": [self.number_of_layers]+[""]*(len_-1),
            "Active nodes per layer": [n for n in self.__number_of_nodes_mapping[:-1]],
            "Activate edges per layer": [n for n in self.__number_of_edges_mapping[:-1]],
        }

        return tabulate(str_, headers="keys", tablefmt="psql")

    def __eq__(self, other):
        if not isinstance(other, MultiplexCore):
            return NotImplemented

        if self._multiplex_dict.keys() != other._multiplex_dict.keys():
            return False

        for idx_ in self._multiplex_dict:
            if self._multiplex_dict[idx_] != other._multiplex_dict[idx_]:
                return False

        return True


    # ~~~ Public method to calculate structural measures ~~~
    def get_node_edge_counts(self):
        # Find union of all layers
        composed_ = nx.compose_all([layer.graph for layer in self.multiplex])

        # Get layerwise counts
        node_counts = [layer.graph.number_of_nodes() for layer in self.multiplex]
        edge_counts = [layer.graph.number_of_edges() for layer in self.multiplex]

        # Return in order total nodes, total edges, nodes, edges
        return (composed_.number_of_nodes(),
            composed_.number_of_edges(),
            node_counts,
            edge_counts
        )


    # ~~~ Public methods to get alternative structs ~~~
    def get_supraadjacency(self):
        N_ = self.number_of_nodes

        # Create block matrix of all N_ x N_ identities
        L_ = self.number_of_layers
        supraadjency = np.tile(np.identity(N_), (L_, L_))

        # Fill in layer-wise adjacency matrices
        for idx_, network in enumerate(self.multiplex):
            ## ? May be able to clean this up with nx.to_numpy_array
            ## ? with additional nodelist argument?
            ## Get each layer's adjacency matrix
            adjacency_ = np.identity(N_)

            ## Fill in entries where an edge exists
            for edge in network.graph.edges:
                adjacency_[edge] = 1

            ## Determine where in block matrix it belongs
            idx = idx_ % L_

            ## Add it to appropriate slice
            supraadjency[idx*N_:(idx+1)*N_, idx*N_:(idx+1)*N_] = adjacency_

        return supraadjency


# ========================== FUNCTIONS =================================
def read_edgelist(filepath: str, network_type: str = "NETWORK",
                output_type: str = "STANDARD"):
    # Validate inputs
    ## Simplify type strings
    network_type = network_type.upper()
    output_type = output_type.upper()

    ## Check network type is supported
    if network_type not in ["NETWORK", "MULTIPLEX"]:
        raise NotImplementedError(
            f"{network_type} is not a supported network type!"
        )
    ## Check output type is supported
    if output_type not in ["STANDARD", "CLASS"]:
        raise NotImplementedError(
            f"{output_type} is not a supported output type!"
        )

    # Read edgelist
    ## Initialize single-layer as list
    if network_type == "NETWORK":
        ## If specified, convert to class at this stage
        if output_type == "CLASS":
            return NetworkCore(edgelist=edgelist)
        else:
            return edgelist

    ## Initialize multiplex as dict
    else:
        with open(filepath) as fh_:
            lines = fh_.readlines()

        # TODO: Use str.strip() instead?
        lines = [line.rstrip().split(" ") for line in lines]
        multiplex = {int(line[0]): set() for line in lines}
        for line in lines:
            edge = (int(line[1]), int(line[2]))
            multiplex[int(line[0])].add(edge)

        ## If specified, convert to class at this stage
        if output_type == "CLASS":
            return MultiplexCore(multiplex_dict=multiplex)
        else:
            return multiplex