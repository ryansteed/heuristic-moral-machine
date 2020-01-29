from snorkel.labeling import labeling_function
import numpy as np

"""
:param x: a DataFrame containing all the fields of the input DataFrame for two ethical alternatives
:returns: whether or not to intervene (0 or 1); -1 to abstain
"""

# @labeling_function