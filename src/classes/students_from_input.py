import numpy as np 
import pandas as pd 

from student import Student
from student import Team
from student import CompError

student_ids = []

def read_input(file, use_range = False, normalize=True):
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
		
		# Takes care of the case where input comes in as String instead of int.
		if (student[1] == "MBA" or student[1] == 0):
			degree_pursuing = 0
		elif(student[1] == "MEng" or student[1] == 1):
			degree_pursuing = 1

		cs_ug = student[2]

		coding_ability = student[3]
		num_yrs_work_exp = student[4]

		scaled_coding_ability = scaled_coding_abilities[i]
		scaled_num_yrs_work_exp = scaled_yrs_work_experience[i]

		# TODO: check the raw input against our validity checks for Student values before scaling.
		rankings = student[5:15]

		a = Student("Test", ID, degree_pursuing, cs_ug, coding_ability, num_yrs_work_exp, rankings)
		a.check_valid_all()

		if (normalize):
			a = Student("Test", ID, degree_pursuing, cs_ug, scaled_coding_ability, scaled_num_yrs_work_exp, rankings, True)

		students_lst.append(a)

	t = Team(students_lst)


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
	t.do_diversity_calculation()

# NOTE: this exact code is duplicated in student.py. If you make changes here, change there as well.
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


