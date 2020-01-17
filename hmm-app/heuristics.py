from snorkel.labeling import labeling_function
import numpy as np

"""
:param x: a DataFrame containing all the fields of the input DataFrame for two ethical alternatives
:returns: whether or not to intervene (0 or 1); -1 to abstain
"""

characters_all = [
    'Man', 'Woman', 'Pregnant', 'Stroller', 'OldMan', 'OldWoman', 'Boy', 'Girl',\
    'Homeless', 'LargeWoman', 'LargeMan', 'Criminal', 'MaleExecutive', 'FemaleExecutive', \
    'FemaleAthlete', 'MaleAthlete', 'FemaleDoctor', 'MaleDoctor', 'Dog', 'Cat'
]

def choose_max(x):
    """
    Accept a single argmax only; if there is a tie, abstain.

    :param x: an nparray of the values; must be in the order `noint`, `int`
    """
    if len(np.argwhere(x == np.max(x))) > 1: return -1
    return x.argmax()

def choose_barrier(x, reverse=False):
    """
    Choose the scenario where the AV hits the barrier.
    If there is no such scenario, abstain.

    :param reverse: If false, choose to hit the barrier. Else choose not to.
    """
    if x["Barrier_noint"] == 1 and x["Barrier_int"] == 1: return -1
    elif x["Barrier_noint"] == 1: return 0 if not reverse else 1
    elif x["Barrier_int"] == 1: return 1 if not reverse else 0
    return -1

def count_characters(x, suffix, characters):
    """
    :param suffix: The suffix to use - int or noint
    :param characters: a list of characters to sum up
    :return: the number of characters in these groups
    """
    return sum([
        x["{}_{}".format(c, suffix)] for c in characters
    ])

def select_against_homogenous_group(x, group):
    """
    Always select against a group if it contains only instances of characters in :group:.
    """
    only_group = {
        s: count_characters(x, s, characters_all) == count_characters(x, s, group)
        for s in ["noint", "int"]
    }
    if only_group["int"] and only_group["noint"]: return -1
    if only_group["noint"]: return 1
    if only_group["int"]: return 0
    return -1

def spare_group(x, group):
    """
    Never choose an alternative that sacrifices a character in :group:.
    """
    group_member_present = {
        s: count_characters(x, s, group) > 0
        for s in ["noint", "int"]
    }
    if group_member_present["noint"] and group_member_present["int"]: return -1
    if group_member_present["noint"]: return 1
    if group_member_present["int"]: return 0
    return -1

@labeling_function()
def lf_doctors(x):
    """Favor doctors."""
    num_doctors = np.array([
        count_characters(x, suffix, ["MaleDoctor", "FemaleDoctor"]) 
        for suffix in ['noint', 'int']
    ])
    return choose_max(num_doctors)

@labeling_function()
def lf_utilitarian(x):
    """Save the most lives."""
    max_characters = np.array([
        x['NumberOfCharacters_{}'.format(suffix)] 
        for suffix in ['noint', 'int']
    ])
    return choose_max(max_characters)

@labeling_function()
def lf_utilitarian_anthro(x):
    """Save the most lives."""
    max_hoomans = np.array([
        count_characters(x, suffix, [c for c in characters_all if c not in ["Dog", "Cat"]])
        for suffix in ['noint', 'int']
    ])
    return choose_max(max_hoomans)

@labeling_function()
def lf_inaction(x):
    """Never intervene."""
    return 0

@labeling_function()
def lf_pedestrians(x):
    """Favor pedestrians over passengers. (Always choose the barrier.)"""
    return choose_barrier(x)

@labeling_function()
def lf_females(x):
    """Save the most women."""
    num_females = np.array([
        count_characters(x, suf, ["Girl", "FemaleAthlete", "FemaleExecutive", "FemaleDoctor"])
        for suf in ["noint", "int"]
    ])
    return choose_max(num_females)

@labeling_function()
def lf_fitness(x):
    """Favor alternatives where the overall fitness (fit - large) is higher."""
    fitness_score = np.array([
        count_characters(x, suf, ["MaleAthlete", "FemaleAthlete"])\
            - count_characters(x, suf, ["LargeMan", "LargeWoman"])
        for suf in ["noint", "int"]
    ])
    return choose_max(fitness_score)

@labeling_function()
def lf_status(x):
    """Save the most executives."""
    num_rich = np.array([
        count_characters(x, suffix, ["MaleExecutive", "FemaleExecutive"])
        for suffix in ['noint', 'int']
    ])
    return choose_max(num_rich)

@labeling_function()
def lf_legal(x):
    """Do not hit the pedestrians if the pedestrians are crossing legally."""
    # if crossing is explicitly legal (green light)
    if (x["CrossingSignal"] == 1):
        # choose the barrier alternative, if it exists
        return choose_barrier(x)
    return -1

@labeling_function()
def lf_illegal(x):
    """Save the passengers if the pedestrians are crossing illegally."""
    # if crossing is explicitly illegal (red light)
    if (x["CrossingSignal"] == 2):
        # choose not to hit the barrier
        return choose_barrier(x, reverse=True)
    return -1

@labeling_function()
def lf_youth(x):
    """Save the most children."""
    num_children = np.array([
        count_characters(x, suffix, ["Stroller", "Boy", "Girl", "Pregnant"])
        for suffix in ['noint', 'int']
    ])
    return choose_max(num_children)

@labeling_function()
def lf_criminals(x):
    """If either group consists only of criminals, prefer the other."""
    return select_against_homogenous_group(x, ["Criminal"])

@labeling_function()
def lf_homeless(x):
    """If either group consists only of the homeless, prefer the other."""
    return select_against_homogenous_group(x, ["Homeless"])

@labeling_function()
def lf_pets(x):
    """If either group consists only of pets, prefer the other."""
    return select_against_homogenous_group(x, ["Dog", "Cat"])

@labeling_function()
def lf_spare_strollers(x):
    """Spare strollers at all cost."""
    return spare_group(x, ["Stroller"])

@labeling_function()
def lf_spare_girl(x):
    """Spare strollers at all cost."""
    return spare_group(x, ["Girl"])

@labeling_function()
def lf_spare_boy(x):
    """Spare strollers at all cost."""
    return spare_group(x, ["Boy"])

@labeling_function()
def lf_spare_pregnant(x):
    """Spare strollers at all cost."""
    return spare_group(x, ["Pregnant"])

