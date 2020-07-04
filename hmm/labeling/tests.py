import unittest
from .moralmachine import *
from .utils import transform_abstract
import pandas as pd

"""
A collection of unit tests for the labeling functions in `moralmachine.py` and `kidney_exchange.py`.

intervene => save characters with suffix int
don't intervene => save characters with suffix noint
"""
# don't intervene
SAVE_NOINT = NOINT = 0
# intervene
SAVE_INT = INT = 1
# abstain
ABSTAIN = -1


class LabelingFunctionTestCase(unittest.TestCase):
	"""
	Note: A response of 0 indicates that the user chooses not to interfere, thus saving 
	the characters with suffix _noint. A response of 1 indicates the user chooses to interfere, 
	thus saving the characters with suffix _int. A response of -1 indicates abstention.
	"""
	def setUp(self):
		np.random.seed(1)

	def test_doctors(self):
		self.assertEqual(SAVE_NOINT, doctors(self.generate_df_random({
			"Medical_int": 1,
			"Medical_noint": 2
		})))
		self.assertEqual(SAVE_INT, doctors(self.generate_df_random({
			"Medical_int": 5,
			"Medical_noint": 2
		})))
		self.assertEqual(ABSTAIN, doctors(self.generate_df_null()))

	def test_utilitarian(self):
		self.assertEqual(SAVE_NOINT, utilitarian(self.generate_df_random({
			"NumberOfCharacters_int": 0,
			"NumberOfCharacters_noint": 1
		})))
		self.assertEqual(SAVE_INT, utilitarian(self.generate_df_random({
			"NumberOfCharacters_int": 2,
			"NumberOfCharacters_noint": 1
		})))
		self.assertEqual(ABSTAIN, utilitarian(self.generate_df_random({
			"NumberOfCharacters_int": 0,
			"NumberOfCharacters_noint": 0
		})))

	def test_utilitarian_anthro(self):
		self.assertEqual(ABSTAIN, utilitarian_anthro(self.generate_df_null({"Non-human_int": 2})))
		self.assertEqual(SAVE_INT, utilitarian_anthro(self.generate_df_null({"Human_int": 2})))
		self.assertEqual(SAVE_NOINT, utilitarian_anthro(self.generate_df_null({
			"Human_int": 1,
			"Human_noint": 2
		})))

	def test_inaction(self):
		for i in range(3):
			self.assertEqual(SAVE_NOINT, inaction(self.generate_df_random()))

	def test_pedestrians(self):
		self.assertEqual(SAVE_INT, pedestrians(self.generate_df_random({
			"Passenger_int": 0,
			"Passenger_noint": 1
		})))
		self.assertEqual(SAVE_NOINT, pedestrians(self.generate_df_random({
			"Passenger_int": 1,
			"Passenger_noint": 0
		})))
		self.assertEqual(ABSTAIN, pedestrians(self.generate_df_random({
			"Passenger_int": 0,
			"Passenger_noint": 0
		})))
		self.assertEqual(ABSTAIN, pedestrians(self.generate_df_random({
			"Passenger_int": 1,
			"Passenger_noint": 1
		})))

	def test_females(self):
		self.assertEqual(SAVE_INT, females(self.generate_df_null({
			"Female_int": 2
		})))
		self.assertEqual(SAVE_NOINT, females(self.generate_df_null({
			"Female_int": 2,
			"Female_noint": 3
		})))
		self.assertEqual(ABSTAIN, females(self.generate_df_null()))
 
	def test_fitness(self):
		self.assertEqual(ABSTAIN, fitness(self.generate_df_random({
			"Fit_int": 1,
			"Fat_int": 1,
			"Fit_noint": 1,
			"Fat_noint": 1
		})))
		self.assertEqual(SAVE_INT, fitness(self.generate_df_null({
			"Fit_int": 2,
			"Fat_int": 1,
			"Fit_noint": 1,
			"Fat_noint": 2
		})))
		self.assertEqual(SAVE_NOINT, fitness(self.generate_df_null({
			"Fat_int": 1
		})))
		self.assertEqual(ABSTAIN, fitness(self.generate_df_null()))

	def test_status(self):
		self.assertEqual(ABSTAIN, status(self.generate_df_null({
			"Working_int": 2,
			"Working_noint": 2
		})))
		self.assertEqual(SAVE_INT, status(self.generate_df_null({
			"Working_int": 2
		})))
		self.assertEqual(SAVE_NOINT, status(self.generate_df_null({
			"Working_noint": 2
		})))
		self.assertEqual(ABSTAIN, status(self.generate_df_null()))

	def test_legal(self):
		self.assertEqual(ABSTAIN, legal(self.generate_df_random({
			"Law Abiding_int": 0,
			"Law Abiding_noint": 0,
			"Law Violating_int": 0,
			"Law Violating_noint": 0,
			"Passenger_noint": 0,
			"Passenger_int": 0
		})))
		self.assertEqual(ABSTAIN, legal(self.generate_df_random({
			"Law Abiding_int": 0,
			"Law Abiding_noint": 0,
			"Law Violating_int": 0,
			"Law Violating_noint": 0,
			"Passenger_noint": 0,
			"Passenger_int": 0
		})))
		self.assertEqual(INT, legal(self.generate_df_random({
			"Law Abiding_int": 1,
			"Law Abiding_noint": 0,
			"Law Violating_int": 0,
			"Law Violating_noint": 0,
			"Passenger_noint": 1,
			"Passenger_int": 0
		})))
		self.assertEqual(NOINT, legal(self.generate_df_random({
			"Law Abiding_int": 0,
			"Law Abiding_noint": 1,
			"Law Violating_int": 0,
			"Law Violating_noint": 0,
			"Passenger_int": 1,
			"Passenger_noint": 0
		})))
		self.assertEqual(ABSTAIN, legal(self.generate_df_random({
			"Law Abiding_int": 1,
			"Law Abiding_noint": 1,
			"Law Violating_int": 0,
			"Law Violating_noint": 0,
			"Passenger_int": 0,
			"Passenger_noint": 0
		})))

	def test_illegal(self):
		self.assertEqual(ABSTAIN, illegal(self.generate_df_random({
			"Law Violating_int": 0,
			"Law Violating_noint": 0,
			"Passenger_noint": 0,
			"Passenger_int": 0
		})))
		self.assertEqual(ABSTAIN, illegal(self.generate_df_random({
			"Law Violating_int": 1,
			"Law Violating_noint": 1,
			"Passenger_noint": 0,
			"Passenger_int": 0
		})))
		self.assertEqual(INT, illegal(self.generate_df_random({
			"Law Violating_int": 0,
			"Law Violating_noint": 1,
			"Passenger_noint": 0,
			"Passenger_int": 1
		})))
		self.assertEqual(NOINT, illegal(self.generate_df_random({
			"Law Violating_int": 1,
			"Law Violating_noint": 0,
			"Passenger_int": 0,
			"Passenger_noint": 1
		})))

	def test_youth(self):
		self.assertEqual(ABSTAIN, youth(self.generate_df_null()))
		self.assertEqual(SAVE_INT, youth(self.generate_df_null({
			"Young_int": 2,
			"Young_noint": 1
		})))
		self.assertEqual(SAVE_NOINT, youth(self.generate_df_null({
			"Young_int": 1,
			"Young_noint": 2
		})))

	def test_criminals(self):
		# neither group is only composed of criminals
		self.assertEqual(ABSTAIN, criminals(self.generate_df_null({
			"Criminal_int": 3,
			"Criminal_noint": 3,
			"NumberOfCharacters_noint": 4,
			"NumberOfCharacters_int": 4
		})))
		self.assertEqual(SAVE_INT, criminals(self.generate_df_null({
			"Criminal_int": 3,
			"Criminal_noint": 3,
			"NumberOfCharacters_noint": 3,
			"NumberOfCharacters_int": 4
		})))
		self.assertEqual(SAVE_NOINT, criminals(self.generate_df_null({
			"Criminal_int": 3,
			"Criminal_noint": 3,
			"NumberOfCharacters_int": 3,
			"NumberOfCharacters_noint": 4
		})))

	def test_homeless(self):
		# neither group is only composed of homeless
		self.assertEqual(ABSTAIN, homeless(self.generate_df_null({
			"Homeless_int": 3,
			"Homeless_noint": 3,
			"NumberOfCharacters_noint": 4,
			"NumberOfCharacters_int": 4
		})))
		self.assertEqual(SAVE_INT, homeless(self.generate_df_null({
			"Homeless_int": 3,
			"Homeless_noint": 3,
			"NumberOfCharacters_noint": 3,
			"NumberOfCharacters_int": 4
		})))
		self.assertEqual(SAVE_NOINT, homeless(self.generate_df_null({
			"Homeless_int": 3,
			"Homeless_noint": 3,
			"NumberOfCharacters_int": 3,
			"NumberOfCharacters_noint": 4
		})))

	def test_pets(self):
		# neither group is only composed of pets
		self.assertEqual(ABSTAIN, pets(self.generate_df_null({
			"Non-human_int": 3,
			"Non-human_noint": 3,
			"NumberOfCharacters_noint": 4,
			"NumberOfCharacters_int": 4
		})))
		self.assertEqual(SAVE_INT, pets(self.generate_df_null({
			"Non-human_int": 3,
			"Non-human_noint": 3,
			"NumberOfCharacters_noint": 3,
			"NumberOfCharacters_int": 4
		})))
		self.assertEqual(SAVE_NOINT, pets(self.generate_df_null({
			"Non-human_int": 3,
			"Non-human_noint": 3,
			"NumberOfCharacters_int": 3,
			"NumberOfCharacters_noint": 4
		})))

	def test_spare_group(self):
		# using strollers as an example
		self.assertEqual(ABSTAIN, spare_strollers(self.generate_df_null()))
		self.assertEqual(ABSTAIN, spare_strollers(self.generate_df_random({
			"Infancy_int": 1,
			"Infancy_noint": 2
		})))
		self.assertEqual(SAVE_INT, spare_strollers(self.generate_df_random({
			"Infancy_int": 1,
			"Infancy_noint": 0
		})))
		self.assertEqual(SAVE_NOINT, spare_strollers(self.generate_df_random({
			"Infancy_int": 0,
			"Infancy_noint": 2
		})))


#    labeling_functions.illegal,
#    labeling_functions.youth,
#    labeling_functions.criminals,
#    labeling_functions.homeless,
#    labeling_functions.pets,
#    labeling_functions.spare_strollers,
#    labeling_functions.spare_girl,
#    labeling_functions.spare_boy,
#    labeling_functions.spare_pregnant


	@staticmethod
	def generate_df_null(subdict={}):
		return LabelingFunctionTestCase.df_from_dict({
			'{}_{}'.format(c, s): 0 for c in characters_abstract for s in ["int", "noint"]
		}, subdict)

	@staticmethod
	def generate_df_random(subdict={}):
		return LabelingFunctionTestCase.df_from_dict({
			'{}_{}'.format(c, s): np.random.randint(5) for c in characters_abstract for s in ["int", "noint"]
		}, subdict)

	@staticmethod
	def df_from_dict(d, subd):
		d.update(subd)
		return pd.DataFrame([d]).iloc[0]


if __name__ == "__main__":
	unittest.main()
