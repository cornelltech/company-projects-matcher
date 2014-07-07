import numpy as np 
import pandas as pd 

from classes import Student
from classes import Team
from classes import Project
from classes import CompError

student_ids = []

def read_input(file, normalize=True):
	data = pd.read_csv(file)
	data_array = np.array(data)
	shape = data_array.shape
	num_rows = shape[0]

	# Normalize our numerical variables to lie between 0 and 1.
	all_coding_abilities = data_array[:,3]
	all_work_experience = data_array[:,4]

	# TODO: instead of normalizing, should just scale it out of 1.
	# Normalization is too dependent on the values it's passed in with.
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
		coding_ability = student[3]
		num_yrs_work_exp = student[4]
		rankings = student[5:15]

		scaled_coding_ability = scaled_coding_abilities[i]
		scaled_num_yrs_work_exp = scaled_yrs_work_experience[i]

		a = Student("Test", ID, degree_pursuing, cs_ug, coding_ability, num_yrs_work_exp, rankings)

		if (normalize):
			a = Student("Test", ID, degree_pursuing, cs_ug, scaled_coding_ability, scaled_num_yrs_work_exp, rankings, True)

		students_lst.append(a)

	t = Team(students_lst)
	Team.print_team(t)


	# print "The technical rating was calculated using each student's coding ability, undergraduate major (CS or not),"
	# print "number of years of work experience, and degree pursuing. "
	# print ""

	# print "This team's technical rating is:", 
	# print Team.calculate_technical_rating(t)

	# print ""
	# print ""

	# print "The average interest rating for a project was calculated based on how high each student ranked the "
	# print "project, and averaging these values together."

	# print "For project with ID 2665, this team's average interest rating is:",

	# print t.calculate_interest_rating(2665)

	# print ""

	# print "For project with ID 3250, this team's average interest rating is:",

	# print t.calculate_interest_rating(3250)

	# print ""

	# print "Process completed."

	# print ""
	# print ""

	#print t.calculate_pairwise_differences([0, 1, 1, 0])
	
	#t.pretty_print_properties()
	#t.do_diversity_calculation()
	#print "If we divide by 4 the weighted average is",
	#print (weighted_avg * 1.0)/4

	# 		def __init__(self, ID, num_MBAs, num_MEngs):
	p = Project(1300, 4, 2)
	print p.ID
	print p.num_MEngs
	print p.num_MBAs
	print "p has " + str(p.remaining_MEng_spots) + " MEng spots remaining."
	p.add_student_to_MEngs(students_lst[0])
	print "After add, p has " + str(p.remaining_MEng_spots) + " MEng spots remaining."
	print [s.get_student_properties() for s in p.MEng_list]

	#p.add_student_to_MEngs(students_lst[0])
	p.add_student_to_MEngs(students_lst[1])
	p.add_student_to_MEngs(students_lst[3])
	print [s.get_student_properties() for s in p.MEng_list]
	print len(p.MEng_list)

# NOTE: this exact code is duplicated in student.py. If you make changes here, change there as well.
def normalize_bet_zero_and_one(lst):
	lst_max = lst.max()
	lst_min = lst.min()
	den = lst_max - lst_min
	num = [elm - lst_min for elm in lst]
	# TODO: get rid of this stupid error.
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
	read_input("new_name.csv", True)


