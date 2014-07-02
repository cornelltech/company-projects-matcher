import numpy as np 
import pandas as pd 
import random
import sklearn

from student import Student
from student import Team

student_ids = []

class CompError(Exception):
	def __init__(self, value):
		self.val = value
	def __str__(self):
		return repr(self.val)

def read_input(file, use_range = False):
	data = pd.read_csv(file)
	data_array = np.array(data)
	shape = data_array.shape
	num_rows = shape[0]

	# Normalize our numerical variables to lie between 0 and 1.
	all_coding_abilities = data_array[:,3]
	all_work_experience = data_array[:,4]

	if (use_range):
		scaled_coding_abilities = scale_inputs_based_on_range(all_coding_abilities)
		scaled_yrs_work_experience = scale_inputs_based_on_range(all_work_experience)

	else:
		scaled_coding_abilities = normalize_bet_zero_and_one(all_coding_abilities)
		scaled_yrs_work_experience = normalize_bet_zero_and_one(all_work_experience)
	
	students_lst = []

	# Extract rows
	for i in range(0, num_rows):
		student = data_array[i,:]
		ID 	= student[0]
		if (ID in student_ids):
			raise CompError("Student IDs must be unique.")
		student_ids.append(ID)
		degree_pursuing = student[1]
		cs_ug = student[2]
		coding_ability = scaled_coding_abilities[i]
		num_yrs_work_exp = scaled_yrs_work_experience[i]
		rankings = student[5:15]
 
		a = Student("Test", ID, degree_pursuing, cs_ug, coding_ability, num_yrs_work_exp, rankings, True)
		students_lst.append(a)

	t = Team(students_lst)
	#Team.print_team(t)
	Team.calculate_technical_rating(t)

	print students_lst[0].get_ranking(2665)

def normalize_bet_zero_and_one(lst):
	lst_max = lst.max()
	lst_min = lst.min()
	den = lst_max - lst_min
	num = [elm - lst_min for elm in lst]
	if (den == 0):
		raise CompError("In normalizing our quantitative variables, all values are the same.")
	final = [(elm * 1.0) / den for elm in num]
	return final

# Scales based on range between -1 and 1.
def scale_inputs_based_on_range(lst):
	b = lst.max() - lst.min()
	if (b == 0):
		raise CompError("In normalizing our quantitative variables, all values are the same.")

	a = lst - lst.mean()

	# print (lst - lst.mean()) / (lst.max() - lst.min())
	normalized = a / b
	return normalized

# Scales between -1 and 1, with mean 0 and variance 1.
def calc_z_score(lst):
	m = lst.mean()
	sd = np.std(lst)
	return (lst - m) / sd

if __name__ == "__main__":
	read_input("new_name.csv")
