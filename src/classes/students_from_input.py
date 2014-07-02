import numpy as np 
import pandas as pd 
import random

from student import Student
from student import Team

def read_input(file):
	data = pd.read_csv(file)
	data_array = np.array(data)
	shape = data_array.shape
	num_rows = shape[0]

	students_lst = []

	# Extract rows
	for i in range(0, num_rows):
		student = data_array[i,:]
		ID 	= student[0]
		degree_pursuing = student[1]
		cs_ug = student[2]
		coding_ability = student[3]
		num_yrs_work_exp = student[4]
		rankings = student[5:15]
 
		a = Student("Test", ID, degree_pursuing, cs_ug, coding_ability, num_yrs_work_exp, rankings)
		students_lst.append(a)


	for a in students_lst:
		print a.get_student_properties()

if __name__ == "__main__":
	read_input("new_name.csv")