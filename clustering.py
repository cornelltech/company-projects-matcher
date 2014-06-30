print (__doc__)

import numpy as np 
import pandas as pd 
from matplotlib import pyplot

from sklearn import preprocessing
from sklearn.cluster import k_means_

def __init__(file):
	# print the full array instead of truncating
	# np.set_printoptions(threshold=np.nan)
	
	""" Extract data from CSV file and place into numpy array. """
	initial_array = pd.read_csv(file)
	data_array = np.array(initial_array)
	print data_array
	return data_array

def do_preprocessing(data_array):
	""" Create a one-hot encoder, and encode the categorical data. Note: the quantitative data is
		placed at the right side of the resulting matrix. """

	enc = preprocessing.OneHotEncoder(categorical_features = [True, False, True, False, False, False])
	enc.fit(data_array)

	#For 'survey_responses.csv,' this produces a 49 x 15 matrix. The last 4 columns are our quantitative data.
	one_hot_data = enc.transform(data_array).toarray()

	#print "The parameters are: " + str(enc.get_params())
	
	#print "The feature indices are: "
	#print enc.feature_indices_

	#print "The number of values is " 
	#print enc.n_values

	#print "The one hot data is " 
	#print one_hot_data
	return one_hot_data

def do_normalize(data_array):
	"""" Normalize the data before feeding into K means. """
	norm = preprocessing.Normalizer()
	normalized = norm.fit_transform(data_array)

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
	data_array = __init__('survey_responses.csv')
	print "Length of data array is "
	print len(data_array)
	pre_processed = do_preprocessing(data_array)
	normalized = do_normalize(pre_processed)
	km = do_k_means(normalized, 3)
	#plot_k_means(km)
