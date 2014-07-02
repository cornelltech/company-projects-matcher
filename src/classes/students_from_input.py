import numpy as np 
import pandas as pd 
import random
import sklearn

from student import Student
from student import Team

class CompError(Exception):
	def __init__(self, value):
		self.val = value
	def __str__(self):
		return repr(self.val)

def read_input(file):
	data = pd.read_csv(file)
	data_array = np.array(data)
	shape = data_array.shape
	num_rows = shape[0]

	# Normalize our numerical variables to lie between 0 and 1.
	all_coding_abilities = data_array[:,3]
	print "all coding abilities is "
	print all_coding_abilities
	temp = scale_inputs(all_coding_abilities)
	for i in range (0, len(all_coding_abilities)):
		data_array[i, 3] = temp[i]
	# print "temp is ",
	# print temp
	# data_array.replace(all_coding_abilities, temp)
	
	# TODO: why won't this reset things? find out.
	print "After normalization, our data array is ",
	print data_array

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


	#for a in students_lst:
		#print a.get_student_properties()

# Scales all inputs to a common scale between 0 and 1.
def scale_inputs(lst):
	b = lst.max() - lst.min()
	if (b == 0):
		raise CompError("In coding abilities, all values are the same.")

	print "List minus the mean"
	a = lst - lst.mean()
	print a

	# print (lst - lst.mean()) / (lst.max() - lst.min())
	return a / b

if __name__ == "__main__":
	read_input("new_name.csv")