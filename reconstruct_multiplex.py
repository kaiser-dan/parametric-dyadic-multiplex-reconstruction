"""Interface script?

Take in following:
- Filehandle for aggregate
- Filehandle for partial observations (if applicable)
- Filehandle for degree sequences (if applicable)
- config file for reconstruction parameters
    - Total number nodes
    - Number of layers in reconstruction
- How to output (pickled multiplex, just multiplex)

Check integrity of all of these things

@author Daniel Kaiser. Created on 2022-04-10. Last modified 2022-04-14.
"""
# ===================== IMPORTS =======================
# Standard library
import argparse
from datetime import datetime

# Scientific computing
import numpy as np

# Network science
import networkx as nx

# Custom modules
from src.DC import reconstruct_from_aggregate_via_observations as reconstruct_observations
from src.DC import reconstruct_from_aggregate_via_degrees as reconstruct_degrees
from utils.validate import validate_observations
from utils.validate import validate_degrees

# Miscelleaneous
## Imports

## Aliases
now = datetime.now


# ===================== METADATA ======================
__author__ = "Daniel Kaiser"
__credits__ = ["Daniel Kaiser", "Siddharth Patwardhan", "Filippo Radicchi"]
__version__ = "1.1.0"
__maintainer__ = "Daniel Kaiser"
__email__ = "kaiserd@iu.edu"
__status__ = "Development"

# ==================== FUNCTIONS =======================
def main(args):
    # Set up reconstruction call
    ## Instantiate aggregate graph object
    agg = nx.read_edgelist(args.file, nodetype=int)

    # Apply reconstruction
    ## Handle reconstruction utilizing partial observations
    if args.partial_observations is not None:
        additional_information_fh = args.partial_observations
        if not validate_observations(agg, additional_information_fh):
            raise ValueError("Partial observations fail validation!")

        reconstruction_multiplex = \
            reconstruct_observations(
                aggregate=agg,
                additional_information_fh=additional_information_fh,
                use_community_detection=args.use_community_detection
            )
    ## Handle reconstruction utilizing layerwise degree sequences
    else:
        additional_information_fh = args.degree_sequences
        if not validate_degrees(additional_information_fh):
            raise ValueError("Degree sequences fail validation!")

        reconstruction_multiplex = \
            reconstruct_degrees(
                aggregate=agg,
                additional_information_fh=additional_information_fh,
                use_community_detection=args.use_community_detection
            )

    # ! >>>> DEBUG >>>>
    print(reconstruction_multiplex)
    
    # ! <<<< DEBUG <<<<

    # Save to file
    # if args.output_type == "edgelist":
    #     reconstruction_multiplex.save_edgelist(args.output)
    # elif args.output_type == "pickle":
    #     reconstruction_multiplex.save_pickle(args.output)


# ====================== MAIN ==========================
if __name__ == "__main__":
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="Dyadic multiplex reconstruction command-line interface. NOTE: All delimeters are presumed to be a single space.")

    # Add required flags (file handling)
    parser.add_argument(
        "-f", "--file",
        type=str,
        required=True,
        help="Filehandle for aggregate network edgelist."
        )
    parser.add_argument(
        "-o", "--output",
        type=str,
        required=True,
        help="Filehandle for output reconstructed multiplex edgelist."
    )
    parser.add_argument(
        "-t", "--output-type",
        type=str,
        choices=["edgelist", "pickle"],
        required=True,
        help="Indicator of how output file should be formatted. Options are either an edgelist or a pickled Multiplex class."
    )

    # Add partial information mutually-exclusive group
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-p", "--partial-observations",
        type=str,
        help="Filehandle of multiplex edgelist for a priori known/observed multiplex structure."
    )
    group.add_argument(
        "-d", "--degree-sequences",
        type=str,
        help="Filehandle of degree sequences per layer. Each line is presumed to be the total degree sequence (over all nodes, active or not in that layer) for a given layer, ordered."
    )

    # Add optional arguments
    parser.add_argument(
        "-c", "--use-community-detection",
        action="store_true",
        help="Indicator flag on if community detection should be used to aid reconstruction."
    )

    # Parse arguements
    args = parser.parse_args()

    # Validate arguments
    # validate_thing(stuff) -> (bool, None or Error)

    validations_ = [
        validate_observations(0, 0),
        validate_degrees(0),  # Don't need both, fill in others
    ]
    validations, err_msgs = zip(*validations_)

    # Run reconstruction
    ## If validations pass, apply reconstruction
    if all(validations):
        main(args)

    ## If validations fail, log error messages
    else:
        errors_ = "error_{}.log".format(now().strftime("%Y-%m-%d_%H:%M:%S"))
        with open(errors_, "w") as fh_:
            for msg in np.where(err_msgs is not None):
                fh_.write(msg)
        print(f"Invalid parameters/partial information! See {errors_} for details.")