from snorkel.labeling import labeling_function
import numpy as np
from utils import *

"""
:param x: a DataFrame containing all the fields of the input DataFrame for two ethical alternatives
:returns: whether or not to intervene (0 or 1); -1 to abstain
"""

characters_all = [
    'Man', 'Woman', 'Pregnant', 'Stroller', 'OldMan', 'OldWoman', 'Boy', 'Girl',\
    'Homeless', 'LargeWoman', 'LargeMan', 'Criminal', 'MaleExecutive', 'FemaleExecutive', \
    'FemaleAthlete', 'MaleAthlete', 'FemaleDoctor', 'MaleDoctor', 'Dog', 'Cat'
]

@labeling_function()
def doctors(x):
    """Favor doctors."""
    num_doctors = np.array([
        count_characters(x, suffix, ["MaleDoctor", "FemaleDoctor"]) 
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
        count_characters(x, suffix, [c for c in characters_all if c not in ["Dog", "Cat"]])
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
        count_characters(x, suf, ["Girl", "FemaleAthlete", "FemaleExecutive", "FemaleDoctor"])
        for suf in ["noint", "int"]
    ])
    return choose_max(num_females)

@labeling_function()
def fitness(x):
    """Favor alternatives where the overall fitness (fit - large) is higher."""
    fitness_score = np.array([
        count_characters(x, suf, ["MaleAthlete", "FemaleAthlete"])\
            - count_characters(x, suf, ["LargeMan", "LargeWoman"])
        for suf in ["noint", "int"]
    ])
    return choose_max(fitness_score)

@labeling_function()
def status(x):
    """Save the most executives."""
    num_rich = np.array([
        count_characters(x, suffix, ["MaleExecutive", "FemaleExecutive"])
        for suffix in ['noint', 'int']
    ])
    return choose_max(num_rich)

@labeling_function()
def legal(x):
    """Do not hit the pedestrians if the pedestrians are crossing legally."""
    # if crossing is explicitly legal (green light)
    if (x["CrossingSignal"] == 1):
        # choose the barrier alternative, if it exists
        return choose_barrier(x)
    return -1

@labeling_function()
def illegal(x):
    """Save the passengers if the pedestrians are crossing illegally."""
    # if crossing is explicitly illegal (red light)
    if (x["CrossingSignal"] == 2):
        # choose not to hit the barrier
        return choose_barrier(x, reverse=True)
    return -1

@labeling_function()
def youth(x):
    """Save the most children."""
    num_children = np.array([
        count_characters(x, suffix, ["Stroller", "Boy", "Girl", "Pregnant"])
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
    return select_against_homogenous_group(x, ["Dog", "Cat"])

@labeling_function()
def spare_strollers(x):
    """Spare strollers at all cost."""
    return spare_group(x, ["Stroller"])

@labeling_function()
def spare_girl(x):
    """Spare strollers at all cost."""
    return spare_group(x, ["Girl"])

@labeling_function()
def spare_boy(x):
    """Spare strollers at all cost."""
    return spare_group(x, ["Boy"])

@labeling_function()
def spare_pregnant(x):
    """Spare strollers at all cost."""
    return spare_group(x, ["Pregnant"])
