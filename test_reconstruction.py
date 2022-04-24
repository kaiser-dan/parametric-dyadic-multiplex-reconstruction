import sys
# sys.path.append("..")

import networkx as nx

from structs.core import read_edgelist
from structs.multiplex import Multiplex
from src.DC import reconstruct_from_aggregate_via_observations as reconstruct
from utils.performance import get_accuracy

if __name__ == "__main__":
    original = read_edgelist("test/data/raw/multiplex.edgelist", "MULTIPLEX", "CLASS")
    aggregate = nx.read_edgelist("test/data/raw/aggregate.edgelist", nodetype=int)

    # accs = []
    # for _ in range(10):
    #     reconstruction = reconstruct(aggregate, "test/data/raw/partial_small.edgelist")
    #     accs.append(get_accuracy(aggregate, reconstruction, original))
    # print("Tiny partial information", accs)

    accs = []
    for _ in range(10):
        reconstruction = reconstruct(aggregate, "test/data/raw/partial_large.edgelist")
        accs.append(get_accuracy(aggregate, reconstruction, original))
    print("Large partial information", accs)

    # ! CURRENT PROBLEM:
    """Nodes in aggregate do not appear in range(0,N).
    It has length N (total uniqe nodes), but some nodes are skipped
    and what not, so indices of a list into node ids is not isomorphism.
    Can either create table tracking such things,
    or force data to be "nice" beforehand
    """