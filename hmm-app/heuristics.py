from snorkel.labeling import labeling_function
import numpy as np

"""
:param x: a DataFrame containing all the fields of the input DataFrame for two ethical alternatives
:returns: whether or not to intervene (0 or 1); -1 to abstain
"""

def argmax_single(x):
    """
    Accept a single argmax only; if there is a tie, abstain.
    """
    if len(np.argwhere(x == np.max(x))) > 1: return -1
    return x.argmax()

def argmin_single(x):
    """
    Accept a single argmin only; if there is a tie, abstain.
    """
    if len(np.argwhere(x == np.min(x))) > 1: return -1
    return x.argmin()

@labeling_function()
def lf_doctors(x):
    """Favor doctors."""
    num_doctors = np.array([x['MaleDoctor_{}'.format(suffix)] + x['FemaleDoctor_{}'.format(suffix)] for suffix in ['int', 'noint']])
    return argmax_single(num_doctors)

@labeling_function()
def lf_utilitarian(x):
    """Favor saving more lives."""
    max_characters = np.array([x['NumberOfCharacters_{}'.format(suffix)] for suffix in ['int', 'noint']])
    return argmax_single(max_characters)

@labeling_function()
def lf_inaction(x):
    """Never intervene."""
    return 0

@labeling_function()
def lf_pedestrians(x):
    """Favor pedestrians over anything else. (Always choose the barrier.)"""
    if x["Barrier_noint"] == 1 and x["Barrier_int"] == 1: return -1
    else if x["Barrier_noint"] == 1: return 0
    else if x["Barrier_int"] == 1: return 1
    return -1

