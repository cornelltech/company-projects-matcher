print (__doc__)

import numpy as np 
import pandas as pd 
from matplotlib import pyplot

from sklearn import preprocessing
from sklearn.cluster import k_means_

def __init__(file):
	# print the full array instead of truncating
	# np.set_printoptions(threshold=np.nan)
	
	# Extract data from CSV file and place into array.
	pre_one_hot = pd.read_csv(file)
	data_array = np.array(pre_one_hot)
	print "init"
	return data_array

def do_preprocessing(data_array):
	
	# Create encoder, and encode the data.
	enc = preprocessing.OneHotEncoder()
	enc.fit(data_array)
	one_hot_data = enc.transform(data_array) #
	return one_hot_data

def do_k_means(one_hot_data, k):
	kmeans = k_means_.KMeans(n_clusters=k)
	kmeans.fit(one_hot_data)

	print kmeans.labels_ # describing the data points
	print kmeans.cluster_centers_ # what does this mean?

	return kmeans

def plot_k_means(kmeans):
	print "in plot function"
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

	print "Performed kmeans."

	print "The labels are: "
	print kmeans.labels_

	print "The centroids are: "
	print kmeans.cluster_centers_


if __name__ == "__main__":
	d = __init__('surveyresponsesedited.csv')
	data = do_preprocessing(d)
	km = do_k_means(data, 3)
	plot_k_means(km)
