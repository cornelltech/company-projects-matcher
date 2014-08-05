import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

default_file = "/Users/ameyaacharya/Documents/Projects/Company Projects/Code/company-projects-matcher/data/survey_responses_altered.csv"

 
def make_hist(file):
	# Extract data
	data = pd.read_csv(file)
	data_array = np.array(data)
	ug_major = data_array[:,0]
	degree_pursuing = data_array[:,2]

	# Make ug_major histogram
	plt.figure()
	plt.hist(ug_major, 8, histtype='bar')
	plt.title('Undergraduate Major')
	plt.show()

	# Make ug_major histogram
	plt.figure()
	plt.hist(degree_pursuing, bins=[0, 1, 2, 3], histtype='bar')
	plt.title('Degree Pursuing')
	plt.text(0.45, 23.5, 'MBA')
	plt.text(1.45, 22.5, 'MEng')
	plt.text(2.45, 4.5, 'MS')
	plt.show()

if __name__ == "__main__":
	make_hist(default_file)