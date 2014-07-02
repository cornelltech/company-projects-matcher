import numpy as np 
import pandas as pd 
import random

from student import Student
from student import Team

def read_input(file):
	data = pd.read_csv(file)
	data_array = np.array(data)

	# Extract rows
	student = data_array[0,:]
	ID 	= student[0]
	degree_pursuing = student[1]
	cs_ug = student[2]
	coding_ability = student[3]
	num_yrs_work_exp = student[4]
	rankings = student[5:15]

# 	def __init__ (self, name, ID, degree_pursuing, cs_ug, cod_abil, num_yrs_work_exp, project_lst):
 
	a = Student("Test", ID, degree_pursuing, cs_ug, coding_ability, num_yrs_work_exp, rankings)
	print a.name
	print a.ID
	print a.degree_pursuing
	print a.coding_ability
	print a.was_cs_ug
	print a.work_experience
	print a.project_rankings

if __name__ == "__main__":
	read_input("new_name.csv")