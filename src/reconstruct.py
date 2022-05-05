"""
@author Daniel Kaiser. Created on 2022-05-05.
"""
# ===================== IMPORTS =======================
# Standard library
import random

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
    pass

def get_partitions(remnants):
    pass


# ----------------- Drivers ----------------
def reconstruct_from_observations(aggregate, observations=None,
        use_community_detection=False, soft_classifications=False):
    pass



"""
def partial_information_experiment(G,exp_type,iterations=10):
    #G: [g1,g2]
    #exp_type: 'd' or 'cd'
    A,partial_info=set(G[0].edges()).symmetric_difference(set(G[1].edges())),np.linspace(0,0.95,10)
    GE1,GE2=set(G[0].edges),set(G[1].edges)

    aucs = []
    for info in partial_info:
        aucs_ = []
        for _ in range(iterations):

            kE=set(random.sample(A,int(len(A)*info)))

            kE1=kE.intersection(GE1)
            kE2=kE.intersection(GE2)

            k1 = A.difference(kE2)
            k2 = A.difference(kE1)

            nodes_k1 = [edge[0] for edge in k1] + [edge[1] for edge in k1]
            nodes_k2 = [edge[0] for edge in k2] + [edge[1] for edge in k2]
            nodes_common = set(nodes_k1) | set(nodes_k2)

            G1_remnant,G2_remnant=nx.Graph(),nx.Graph()
            G1_remnant.add_nodes_from(nodes_common)
            G2_remnant.add_nodes_from(nodes_common)
            G1_remnant.add_edges_from(k1)
            G2_remnant.add_edges_from(k2)

            d1,d2=G1_remnant.degree(),G2_remnant.degree()

            if exp_type=='cd':
                partition1 = louvain(G1_remnant).to_node_community_map()
                partition1 = {key: value[0] for key, value in partition1.items()}
                partition2 = louvain(G2_remnant).to_node_community_map()
                partition2 = {key: value[0] for key, value in partition2.items()}

                pin1,pout1=0,0
                for edge in G1_remnant.edges():
                    if partition1[edge[0]]==partition1[edge[1]]:
                        pin1+=1
                    else:
                        pout1+=1
                pin2,pout2=0,0
                for edge in G2_remnant.edges():
                    if partition2[edge[0]]==partition2[edge[1]]:
                        pin2+=1
                    else:
                        pout2+=1
                mu=0.5
                if (pin1+pin2+pout1+pout2)>0:
                    mu=(pin1+pin2)/(pin1+pin2+pout1+pout2)

            classification=[]
            guesses = 0
            ground_truth=[]
            for edge in A.difference(kE):
                if edge in GE1:
                    ground_truth.append(0)
                elif edge in GE2:
                    ground_truth.append(1)
                if exp_type=='d':

                    p1=(d1[edge[0]]*d1[edge[1]]/(d1[edge[0]]*d1[edge[1]]+d2[edge[0]]*d2[edge[1]]))
                    p2=(d2[edge[0]]*d2[edge[1]]/(d1[edge[0]]*d1[edge[1]]+d2[edge[0]]*d2[edge[1]]))
                    if p1>p2:
                        classification.append(0)
                    elif p2>p1:
                        classification.append(1)
                    else:
                        classification.append(random.randint(0,1))

                elif exp_type=='cd':

                    if partition1[edge[0]]==partition1[edge[1]]:
                        p1=(d1[edge[0]]*d1[edge[1]]/(d1[edge[0]]*d1[edge[1]]+d2[edge[0]]*d2[edge[1]]))*mu
                    else:
                        p1=(d1[edge[0]]*d1[edge[1]]/(d1[edge[0]]*d1[edge[1]]+d2[edge[0]]*d2[edge[1]]))*(1-mu)
                    if partition2[edge[0]]==partition2[edge[1]]:
                        p2=(d2[edge[0]]*d2[edge[1]]/(d1[edge[0]]*d1[edge[1]]+d2[edge[0]]*d2[edge[1]]))*mu
                    else:
                        p2=(d2[edge[0]]*d2[edge[1]]/(d1[edge[0]]*d1[edge[1]]+d2[edge[0]]*d2[edge[1]]))*(1-mu)

                    if p1>p2:
                        classification.append(0)
                    elif p2>p1:
                        classification.append(1)
                    else:
                        classification.append(random.randint(0,1))

            aucs_.append(metrics.accuracy_score(ground_truth, classification))
        aucs.append(np.mean(aucs_))

    return aucs
"""