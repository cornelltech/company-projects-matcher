print (__doc__)

import numpy as np 
import pandas as pd 
from sklearn import preprocessing

class ClusteringError(Exception):
	def __init__(self, value):
		self.val = value
	def __str__(self):
		return repr(self.val)

def __init__(file, verbose = False):
	'''
		Returns the relevant info and the IDs for use in distance.py.
	'''
	# Extract data from CSV file and place into numpy array. 
	initial_array = pd.read_csv(file)
	data_array = np.array(initial_array)
	IDs = data_array[:,0]
	relevant_data = data_array[:,[1, 2, 3, 4]]

	if (verbose):
		print relevant_data, IDs
	return (relevant_data, IDs)

def do_preprocessing(data_array_tup, verbose = False):
	''' Creates a one-hot encoder, and encodes the categorical data.

		Parameters
		----------
		data_array_tup: a tuple of the form (relevant_data, IDs).
						This is the return type of __init__.
		verbose: indicates if we want to print updates (bool).

		Returns
		-------
		tuple of form (one_hot_data, dict_key_vals).
		
		one_hot_data: the matrix of data, converted into numerical form.
		Note: the quantitative data is placed at the right side of this
		one_hot_data matrix.

		dict_key_vals: a dictionary with Student IDs as keys, and preprocessed
		data as values.

	'''
	# This is specifically for the format of data in eighty_students.csv.
	data_array = data_array_tup[0]
	if (verbose):
		print "data array tup is " + str(data_array_tup)
	IDs = data_array_tup[1]
	enc = preprocessing.OneHotEncoder(categorical_features = [True, False, True, False])
	enc.fit(data_array)

	one_hot_data = enc.transform(data_array).toarray()
	if (verbose):
		print "OH data is " + str(one_hot_data)

	if (not(len(IDs) == len(data_array))):
		raise ClusteringError("IDs is not the same length as our data array.")
	else:
		dict_key_vals = {}
		counter = 0
		for ID in IDs:
			dict_key_vals[ID] = one_hot_data[counter]
			counter += 1
		if (verbose):
			print dict_key_vals

	return (one_hot_data, dict_key_vals)
