import numpy as np

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
        s: x["NumberOfCharacters_{}".format(s)] == count_characters(x, s, group)
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
    if group_member_present["noint"]: return 0
    if group_member_present["int"]: return 1
    return -1
