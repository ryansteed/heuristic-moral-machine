from snorkel.labeling import labeling_function
import numpy as np
from .utils import *
from ..classification import *

"""
:param x: a DataFrame containing all the fields of the input DataFrame for two ethical alternatives
:returns: whether or not to intervene (0 or 1); -1 to abstain
"""

@labeling_function()
def doctors(x):
    """Favor doctors."""
    num_doctors = np.array([
        x["Medical_{}".format(suffix)]
        for suffix in ['noint', 'int']
    ])
    return choose_max(num_doctors)

@labeling_function()
def utilitarian(x):
    """Save the most lives."""
    max_characters = np.array([
        x['NumberOfCharacters_{}'.format(suffix)] 
        for suffix in ['noint', 'int']
    ])
    return choose_max(max_characters)

@labeling_function()
def utilitarian_anthro(x):
    """Save the most lives."""
    max_hoomans = np.array([
        x["Human_{}".format(suffix)]
        for suffix in ['noint', 'int']
    ])
    return choose_max(max_hoomans)

@labeling_function()
def inaction(x):
    """Never intervene."""
    return 0

@labeling_function()
def pedestrians(x):
    """Favor pedestrians over passengers. (Always choose the barrier.)"""
    return choose_barrier(x)

@labeling_function()
def females(x):
    """Save the most women."""
    num_females = np.array([
        count_characters(x, suf, ["Female"])
        for suf in ["noint", "int"]
    ])
    return choose_max(num_females)

@labeling_function()
def fitness(x):
    """Favor alternatives where the overall fitness (fit - large) is higher."""
    fitness_score = np.array([
        count_characters(x, suf, ["Fit"])\
            - count_characters(x, suf, ["Fat"])
        for suf in ["noint", "int"]
    ])
    return choose_max(fitness_score)

@labeling_function()
def status(x):
    """Save the most executives."""
    num_rich = np.array([
        count_characters(x, suffix, ["Working"])
        for suffix in ['noint', 'int']
    ])
    return choose_max(num_rich)

@labeling_function()
def legal(x):
    """Do not hit the pedestrians if the pedestrians are crossing legally."""
    # if the option is between pedestrians and an AV
    if (x["Passenger_int"] or x["Passenger_noint"]):
        # if crossing is explicitly legal (green light) for the pedestrians
        if (x["Law Abiding_int"] or x["Law Abiding_noint"]):
            # choose the barrier alternative, if it exists
            return choose_barrier(x)
    # otherwise it's peds vs peds - prefer the one following the law
    else:
        # if crossing scenario is the same for both groups, abstain
        if (x["Law Abiding_noint"] == x["Law Abiding_int"] and x["Law Violating_int"] == x["Law Violating_noint"]):
            return -1
        # if one group is crossing illegally, choose against that group
        if x["Law Violating_int"]:
            return SAVE_NOINT
        if x["Law Violating_noint"]:
            return SAVE_INT
        return -1
    return -1

@labeling_function()
def illegal(x):
    """Save the passengers if the pedestrians are crossing illegally."""
    # if passenger vs passenger (shouldn't be possible)
    if x["Passenger_int"] and x["Passenger_noint"]:
        return -1
    # if ped v ped
    elif not (x["Passenger_int"] and x["Passenger_noint"]):
        # return 1 if noint is law violating, 0 if not
        if x["Law Violating_noint"]:
            return 1
        if x["Law Violating_int"]:
            return 0
    # if the choice is between an AV and pedestrians
    else:
        # if the pedestrian group is crossing illegally
        if x["Law Violating_int"]:
            return 0
        if x["Law Violating_noint"]:
            return 1
    return -1

@labeling_function()
def youth(x):
    """Save the most children."""
    num_children = np.array([
        count_characters(x, suffix, ["Young"])
        for suffix in ['noint', 'int']
    ])
    return choose_max(num_children)

@labeling_function()
def criminals(x):
    """If either group consists only of criminals, prefer the other."""
    return select_against_homogenous_group(x, ["Criminal"])

@labeling_function()
def homeless(x):
    """If either group consists only of the homeless, prefer the other."""
    return select_against_homogenous_group(x, ["Homeless"])

@labeling_function()
def pets(x):
    """If either group consists only of pets, prefer the other."""
    return select_against_homogenous_group(x, ["Non-human"])

@labeling_function()
def spare_strollers(x):
    """Spare strollers at all cost."""
    return spare_group(x, ["Infancy"])

# @labeling_function()
# def spare_girl(x):
#     """Spare girls at all cost."""
#     return spare_group(x, ["Girl"])

# @labeling_function()
# def spare_boy(x):
#     """Spare boys at all cost."""
#     return spare_group(x, ["Boy"])

@labeling_function()
def spare_pregnant(x):
    """Spare the pregnant at all cost."""
    return spare_group(x, ["Pregnancy"])

