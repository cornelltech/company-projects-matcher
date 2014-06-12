print (__doc__)

import numpy as np 
import pandas as pd 
import random
from matplotlib import pyplot as plt

def plot_all_data(file):
	data = pd.read_csv(file)
	data_array = np.array(data)

	# Extract columns
	ug_major = data_array[:,0]
	coding_ability = data_array[:,1]
	#degree_pursuing = data_array[:,2]
	num_yrs_work_experience = data_array[:,3]
	group_experience = data_array[:,4]
	m_group_experience = data_array[:,5]

	plot_data(coding_ability, num_yrs_work_experience, 'Coding ability', 'Number of yrs. of work experience', ug_major)
	plot_data(coding_ability, group_experience, 'Coding ability', 'Group experience', ug_major)
	plot_data(coding_ability, m_group_experience, 'Coding ability', 'Multidisc. group experience', ug_major)
	plot_data(num_yrs_work_experience, group_experience, 'Number of yrs. of work experience', 'Group experience', ug_major)
	plot_data(num_yrs_work_experience, m_group_experience, 'Number of yrs. of work experience', 'Multidisc. group experience', ug_major)
	plot_data(group_experience, m_group_experience, 'Group experience experience', 'Multidisc. group experience', ug_major)

def plot_data(xlist, ylist, xlabel, ylabel, shader):
	jitter = 0.2

	i_xlist = [x + random.uniform(-jitter, jitter) for x in xlist]
	plt.scatter(i_xlist, ylist, c=shader, s = 100, edgecolors='None', cmap=plt.cm.hot, alpha = 0.2)
	plt.colorbar()
	plt.title( xlabel + ' vs. ' + ylabel)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.show()
	plt.close()

def plot_colorful_data(xlist, ylist, xlabel, ylabel, shader, is_ug_major = True):
	jitter = 0.2
	
	# If the shader is ug_major
	if is_ug_major:
		colormap = {0: 'r', 1: 'b', 2: 'g', 3: 'y', 4: 'c', 5: 'k', 6:'m', 7:'k'}

	# THIS IS UNSTABLE. SHOULD POSSIBLY FIX.
	# Then the shader must be degree_pursuing
	else:
		colormap = {0: 'y', 1: 'b', 2: 'r'}

	i_xlist = [x + random.uniform(-jitter, jitter) for x in xlist]
	plt.axis([-1, 5, -1, 9])

	for i in range(0, len(i_xlist)):
		plt.plot(i_xlist[i], ylist[i], colormap[shader[i]] + 'o', alpha = 0.7)

	# TEXT
	# plt.text(0, 8, 'Red: ug_major')
	plt.title( xlabel + ' vs. ' + ylabel)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.show()
	plt.close()

def plot_all_colorful_data(file):
	data = pd.read_csv(file)
	data_array = np.array(data)

	# Extract columns
	ug_major = data_array[:,0]
	coding_ability = data_array[:,1]
	degree_pursuing = data_array[:,2]
	num_yrs_work_experience = data_array[:,3]
	group_experience = data_array[:,4]
	m_group_experience = data_array[:,5]

	# Shaded on undergraduate major
	plot_colorful_data(coding_ability, num_yrs_work_experience, 'Coding ability', 'Number of yrs. of work experience', ug_major)
	plot_colorful_data(coding_ability, group_experience, 'Coding ability', 'Group experience', ug_major)
	plot_colorful_data(coding_ability, m_group_experience, 'Coding ability', 'Multidisc. group experience', ug_major)
	plot_colorful_data(num_yrs_work_experience, group_experience, 'Number of yrs. of work experience', 'Group experience', ug_major)
	plot_colorful_data(num_yrs_work_experience, m_group_experience, 'Number of yrs. of work experience', 'Multidisc. group experience', ug_major)
	plot_colorful_data(group_experience, m_group_experience, 'Group experience', 'Multidisc. group experience', ug_major)

	# Shaded on degree pursuing
	plot_colorful_data(coding_ability, num_yrs_work_experience, 'Coding ability', 'Number of yrs. of work experience', degree_pursuing, False)
	plot_colorful_data(coding_ability, group_experience, 'Coding ability', 'Group experience', degree_pursuing, False)
	plot_colorful_data(coding_ability, m_group_experience, 'Coding ability', 'Multidisc. group experience', degree_pursuing, False)
	plot_colorful_data(num_yrs_work_experience, group_experience, 'Number of yrs. of work experience', 'Group experience', degree_pursuing, False)
	plot_colorful_data(num_yrs_work_experience, m_group_experience, 'Number of yrs. of work experience', 'Multidisc. group experience', degree_pursuing, False)
	plot_colorful_data(group_experience, m_group_experience, 'Group experience', 'Multidisc. group experience', degree_pursuing, False)

if __name__ == "__main__":
	plot_all_colorful_data('survey_responses.csv')






