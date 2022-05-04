"""Provides utility to validate specified partial information files
as valid multiplex observations with edges subset of a given aggregate
or as valid degree sequences for some multiplex.

@author Daniel Kaiser. Created on 2022-04-19. Last modified 2022-04-19.
"""
# ===================== IMPORTS =======================
# Standard library
import random
from typing import Union, List

# Scientific computing
import numpy as np

# Network science
import networkx as nx

# Miscelleaneous
from structs.multiplex import Multiplex


# ===================== METADATA ======================
__author__ = "Daniel Kaiser"
__credits__ = [
    "Daniel Kaiser",
]
__version__ = "1.0.0"
__maintainer__ = "Daniel Kaiser"
__email__ = "kaiserd@iu.edu"
__status__ = "Development"


# ===================== FUNCTIONS ==========================
def validate_observations(aggregate, observations):
    return True, None

def validate_degrees(degrees):
    # DO WE NEED AGG TOO?
    return True, None