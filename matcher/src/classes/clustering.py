print (__doc__)

import numpy as np 
import pandas as pd 
from sklearn import preprocessing
from sklearn.cluster import k_means_

default_file = "/Users/ameyaacharya/Documents/Projects/Company Projects/Code/company-projects-matcher/matcher/src/classes/eighty_students.csv"

class ClusteringError(Exception):
	def __init__(self, value):
		self.val = value
	def __str__(self):
		return repr(self.val)


def __init__(file = default_file, verbose = False):
	# print the full array instead of truncating
	# np.set_printoptions(threshold=np.nan)
	# Returns the relevant info and the IDs for use in distance.py
	
	""" Extract data from CSV file and place into numpy array. """
	initial_array = pd.read_csv(file)
	data_array = np.array(initial_array)
	IDs = data_array[:,0]
	relevant_data = data_array[:,[1, 2, 3, 4]]

	# Create a dictionary hashing the student ID to the 

	#print data_array
	if (verbose):
		print relevant_data, IDs
	return (relevant_data, IDs)

def do_preprocessing(data_array_tup, verbose = False):
	""" Create a one-hot encoder, and encode the categorical data. Note: the quantitative data is
		placed at the right side of the resulting matrix. """

	# This is specifically for the format of data in survey_responses.csv.
	# TODO: put this into a global config file.
	data_array = data_array_tup[0]
	if (verbose):
		print "data array tup is " + str(data_array_tup)
	IDs = data_array_tup[1]
	enc = preprocessing.OneHotEncoder(categorical_features = [True, False, True, False])
	enc.fit(data_array)

	#For 'survey_responses.csv,' this produces a 49 x 15 matrix. The last 4 columns are our quantitative data.
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

def do_normalize(data_array, verbose = False):
	"""" Normalize the data before feeding into K means. """
	norm = preprocessing.Normalizer()
	normalized = norm.fit_transform(data_array)

	if (verbose):
		print "mean is "
		print np.mean(data_array, 0)

		print "len mean is "
		print len(np.mean(data_array, 0))

		print normalized

	return normalized

def do_k_means(normalized, k):
	kmeans = k_means_.KMeans(n_clusters=k)
	kmeans.fit_transform(normalized)

	print kmeans.labels_ # describing the data points
	print kmeans.cluster_centers_ # what does this mean?

	return kmeans

def plot_k_means(kmeans):
	print "in plot function"
	# Note: unsure if we want to use a similar straegy.
	# FOR REFERENCE: 
	#for i in range(k):
		#ds = one_hot_data[np.where(labels==i)]
		# pyplot.plot(ds[:,0], ds[:,1], 'o')
		# lines = pyplot.plot(centroids[i,0],centroids[i,1], 'kx')
		# pyplot.setp(lines, ms = 15.0)
		# pyplot.setp(lines, mew = 2.0)


def print_data(enc, transformed, kmeans):
	print "The parameters are: " + str(enc.get_params())
	
	print "The feature indices are: "
	print enc.feature_indices_

	print "The number of values is " 
	print enc.n_values
	
	print "The data is: "
	print transformed.toarray()

	print "The dimensions of the data are: "
	print transformed.shape

	# print "Performed kmeans."

	# print "The labels are: "
	# print kmeans.labels_

	# print "The centroids are: "
	# print kmeans.cluster_centers_


if __name__ == "__main__":
	data_array_tup = __init__()
	#print "Length of data array is "
	#print len(data_array)
	pre_processed_tup = do_preprocessing(data_array_tup)
	pre_processed = pre_processed_tup[0]
	normalized = do_normalize(pre_processed)
	km = do_k_means(normalized, 3)
	#plot_k_means(km)
