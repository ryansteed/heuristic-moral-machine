import numpy as np
import pandas as pd

characters_all = [
    'Man', 'Woman', 'Boy', 'Girl', 'OldMan', 'OldWoman', 'Stroller', 'Pregnant', \
    'LargeMan', 'LargeWoman', 'MaleAthlete', 'FemaleAthlete', 'MaleExecutive', 'FemaleExecutive', \
    'MaleDoctor', 'FemaleDoctor', 'Homeless', 'Criminal', 'Dog', 'Cat'
]
characters_abstract = [
    'Male', 'Female', 'Young', 'Old', 'Infancy', 'Pregnancy',
    'Fat', 'Fit', 'Working', 'Medical', 'Homeless', 'Criminal', 'Human',
    'Non-human'
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
    if x["Passenger_noint"] and x["Passenger_int"]: return -1
    elif x["Passenger_noint"]: return 1 if not reverse else 0
    elif x["Passenger_int"]: return 0 if not reverse else 1
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

def is_passenger(df, suf=''):
    return df['Barrier{}'.format(suf)] == 1

def is_law_abiding(df, suf=''):
    return df['CrossingSignal{}'.format(suf)] == 1 & ~is_passenger(df, suf=suf)

def is_law_violating(df, suf=''):
    return df['CrossingSignal{}'.format(suf)] == 2 & ~is_passenger(df, suf=suf)

def transform_abstract(df):
    A_cols = ["Intervention"] + characters_all + ["Passenger", "Law Abiding", "Law Violating"]
    A_rows = [
        "Intervene", "Male", "Female", "Young", "Old", "Infancy", "Pregnancy", "Fat", "Fit", "Working", "Medical",
        "Homeless", "Criminal", "Human", "Non-human", "Passenger", "Law Abiding", "Law Violating"
    ]
    A = np.matrix([
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    ])
    df['Passenger'] = is_passenger(df)
    df['Law Abiding'] = is_law_abiding(df)
    df['Law Violating'] = is_law_violating(df)
    Theta = np.array(df[A_cols].values)
    f = A.dot(Theta.transpose())
    df = df.drop(labels=A_cols, axis='columns').join(pd.DataFrame(f.transpose(), columns=A_rows, index=df.index), how='inner')
    return df

def pictofy(response, raw=False):
    if raw:
        crossing_light = ["🔴" if is_law_violating(response, suf=suf).iloc[0] else "🟢" if is_law_abiding(response, suf=suf).iloc[0] else " " for suf in ["_noint", "_int"]]
        pedped = ["🚧" if is_passenger(response, suf=suf).iloc[0] else "🚸" for s in ["noint", "int"]]
    else:
        crossing_light = ["🔴" if response["Law Violating_{}".format(suf)].iloc[0] else "🟢" if response["Law Abiding_{}".format(suf)].iloc[0] else " " for suf in ["noint", "int"]]
        pedped = ["🚧" if response["Passenger_{}".format(s)].iloc[0] else "🚸" for s in ["noint", "int"]]
    out_string = \
        "What should the self-driving car do? (ScenarioType: {})\n\n".format(response["ScenarioType"].iloc[0] if "ScenarioType" in response.columns else "Unknown") +\
        "\t    🚘 \n" +\
        "\t   |\t\\ \n" +\
        "\t   v \t v\n" +\
        "\t{}{} \t{}{}\n".format(crossing_light[0], *pedped, crossing_light[1]) +\
        "\t NOINT\tINT\t\n"
    for k, s in {"INT": "int", "NOINT": "noint"}.items():
        out_dict = {col: response["{}_{}".format(col, s)] for col in (characters_all if raw else characters_abstract)}
        out_list = []
        for c, v in out_dict.items():
            if not raw:
                if (int(v)) > 0:
                    out_list.append("{} {}".format(int(v), c.split("_")[0]))
            else:
                for i in range(int(v)):
                    out_list.append(c.split("_")[0])
        out_string += "{} saves: \n{}\n".format(k, out_list)
    print(out_string)