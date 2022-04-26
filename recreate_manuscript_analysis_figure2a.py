"""Script to recreate the analyses presented in the associated manuscript to this repository.

Figure 2a, b marks what the authors concieve of as their "core"
analysis, and in relation to the source code, is undeniably the most
prototypical experimental setting. This script will recreate this
analysis.

@author Daniel Kaiser. Created on 2022-04-26.
"""
# ===================== IMPORTS =======================
# Standard library
import sys
from requests import head
from utils.performance import get_accuracy
sys.path.append(["./", "../"])

# Scientific computing
import numpy as np
import pandas as pd

# Network science
import networkx as nx

# Custom modules
from structs.multiplex import Multiplex
from src.DC import reconstruct_from_aggregate_via_observations as reconstruct
import utils.synthetic as synth

# Miscelleaneous
## Imports
from tabulate import tabulate

## Aliases
plseq = synth.sample_scalefree_sequence
gen_multiplex = synth.get_expected_degree_multiplex

# ==================== FUNCTIONS =======================
def main():
    # Book-keepings
    GAMMAS = [2.67] # 2.00, 2.33, 2.67, 3.00, 3.33]

    # Sample powerlaw degree sequences matching parameters in the paper
    sequences = [
        plseq(exponent=gamma, xmin=3, xmax=np.sqrt(100000), n=100000)
        for gamma in GAMMAS
    ]

    # Generate expected degree duplexes from these sequences
    # * Despite passing in the same degree sequence for each layer, each
    # * layer will be randomly generated form that sequence.
    expected_degree_duplexes = [
        gen_multiplex(sequences=[sequences[idx_]]*2)
        for idx_ in range(len(sequences))
    ]

    # Get XOR aggregates of these duplexes
    aggregates = [
        duplex.aggregate_multiplex("XOR")
        for duplex in expected_degree_duplexes
    ]

    # Save these duplexes and their aggregates to file
    for idx_, gamma in enumerate(GAMMAS):
        expected_degree_duplexes[idx_].save_edgelist(f"recreate-manuscript_ground-truth-duplex_gamma-{gamma}.edgelist")
        aggregates[idx_].save_edgelist(f"recreate-manuscript_aggregate-network_gamma-{gamma}.edgelist")

    # Begin reconstruction experiment
    results_ = {}
    gammas = []
    pfis = []
    accuracies = []

    ## Sweep over gammas
    for idx_, gamma in enumerate(GAMMAS):
        ### Sweep over relative sizes of training set
        for observation_proportion in np.linspace(0, 0.95, 10):
            agg = aggregates[idx_].graph
            multiplex_dict = expected_degree_duplexes[idx_]._multiplex_dict

            #### Set up the proportion of information we will actually use
            observations_ = np.random.choice(range(len(agg.edges)), size=int(observation_proportion*len(agg.edges)))
            observations = [agg.edges[idx_] for idx_ in observations_]

            #### Take observed information and form partial multiplex structure
            partial_multiplex_dict = {layer: [] for layer in multiplex_dict}
            for edge in observations:
                flag = 0
                for layer, edges in multiplex_dict.items():
                    if (not flag) and (edge in set(edges)):
                        partial_multiplex_dict[layer].append(edge)
                        flag = 1

            ##### Save partial obserations to file
            partial_multiplex = Multiplex(multiplex_dict=partial_multiplex_dict)
            partial_multiplex.save_edgelist(f"recreate-manuscript_partial-multiplex_gamma-{gamma}_pfi-{observation_proportion:.2f}.edgelist")

            ##### Apply reconstruction
            reconstruction = reconstruct(aggregate=agg, additional_information_fh=f"recreate-manuscript_partial-multiplex_gamma-{gamma}_pfi-{observation_proportion:.2f}.edgelist")
            accuracy = get_accuracy(aggregate=agg, reconstructed=reconstruction, original=expected_degree_duplexes[idx_])

            #### Track data
            gammas.append(gamma)
            pfis.append(observation_proportion)
            accuracies.append(accuracy)

    ## Save resultant data
    results = pd.DataFrame({
        "Gamma": gammas,
        "ObservationProportion": pfis,
        "ReconstructionAccuracy": accuracies
    })
    results.to_csv("recreate-manuscript_dataframe-accuracies.csv", index=False)

    ## Print for fun
    print(tabulate(results, headers="keys", showindex=False, tablefmt="psql"))


if __name__ == "__main__":
    main()