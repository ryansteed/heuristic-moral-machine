from snorkel.labeling import labeling_function


@labeling_function()
def age(x):
	"""
	Choose the younger patient. All equal, abstain.
	:param x: a DataFrame containing all the fields of the input DataFrame for two ethical alternatives
	:returns: which patient to choose - 0 or 1, -1 to abstain
	"""
	if x["Age_0"] == x["Age_1"]: return -1
	if x["Age_0"] < x["Age_1"]: return 0
	return 1


@labeling_function()
def alcohol(x):
	"""
	Choose the patient who drinks less frequently. All equal, abstain.
	:param x: a DataFrame containing all the fields of the input DataFrame for two ethical alternatives
	:returns: which patient to choose - 0 or 1, -1 to abstain
	"""
	if x["AlcoholConsumption_0"] == x["AlcoholConsumption_1"]: return -1
	if x["AlcoholConsumption_0"] < x["AlcoholConsumption_1"]: return 0
	return 1


@labeling_function()
def health(x):
	"""
	Choose the patient with no history of skin cancer. If the histories are identical, abstain.
	:param x: a DataFrame containing all the fields of the input DataFrame for two ethical alternatives
	:returns: which patient to choose - 0 or 1, -1 to abstain
	"""
	if x["SkinCancer_0"] == x["SkinCancer_1"]: return -1
	if x["SkinCancer_0"]: return 1
	if x["SkinCancer_1"]: return 0

