# TODO: Make this work for arbitrary number of student types. 
# TODO: Make user not have to input the actual student IDs.
#		Can do this by picking the degree with the max
#		number of students. Use this as a parameter to make
#		the matrix of student IDs.
# TODO: Make this work with more than team size.
def create_teams(MBA_student_ids, MEng_student_ids, team_size):
	'''
		A loop that goes through the sample space of students
		and creates teams of students.

		The set of teams teams adhere to our requirements:
			- Plausibility: teams will be formed from selection without 
			replacement (each student is assigned to exactly one team.)
			- Size: Each team will be of a size found in team_sizes.
			- Diversity: each team will have one student of each input type.

		Parameters
		----------

		MBA_student_ids: a list of the student ids of the MBA students.

		MEng_student_ids: a list of the student ids of the MBA students.

		team_size: the target size for teams. If there are extra students left
					at the end, add them to teams:
					This process will create 
						((total_num_students) mod team_size)
					teams with (team_size + 1) students.

					TODO: check this with Greg. 

		Returns
		--------

		teams: a list of tuples that represent teams. Each tuple will contain integers,
				which represent the IDs of the students in the team.
	'''
	
	# if student ID lists are empty or team sizes is empty, error.
	# if the lists are not unique, error.
	# make a list of length toReturn = (total students / team_size) (also integer division is a thing YAY)
	# while there are still teams to make (for i in range (0, toReturn))
	# 	make a temporary team team_creating of [-1] * team_size
	#	team_index = 0
	# 	num_left = team_size
	# 	while num_left > 0
	#		cur_team = None
	# 		generate a random number between 0 and 1.
	#		if the number is greater than 0.5, cur_team is the MBA team.
	#		otherwise, cur_team is the MEng team.
	#		generate a random number r between 0 and len(cur_team)
	#		cur_student_id = cur_team.pop(r) (this is good because it actually removes the ID
	# 							from the original list)
	#		team_creating[team_index] = cur_student_id
	#		team_index += 1
	# 		num_left -= 1
	#	toReturn[i] = team_creating
	# print out the leftover students (iterate through both lists and print IDs)



	print "hi"

# TODO: undefined size thing. Look at TODOs above create_teams.
# def create_student_ids(types_and_sizes):
# 	# Internal method to create student IDs from number of each type of student.

# Parameters
# 		----------

# 		types_and_sizes: a list of tuples of the form (student_type, num_students).
# 						By inputting a specific type of student, you are stating
# 						that you want at least one of that type of student on each
# 						team.

# 						For example: [(MBA, 39), (MEng, 35)].
# 						NOTE: for now the student "type" is really just a string.
# 						Will probably change that later.

# 	cur_id = 0 
# 	student_ids = [[None for x in xrange()]]
# 	for i in range(0, len(types_and_sizes)):
# 		tuple_i = types_and_sizes[i]
# 		num_students_i = tuple_i[1]

# 		print type(range(cur_id, cur_id + num_students_i))

# 		student_ids[i] = range(cur_id, cur_id + num_students_i)
# 		cur_id = num_students_i
# 	return student_ids

	# Note: way for two teams.
	# tuple_one = types_and_sizes[0]
	# tuple_two = types_and_sizes[1]

	# num_students_one = tuple_one[1]
	# num_students_two = tuple_two[1]

	# student_ids_one = range(0, num_students_one)
	# student_ids_two = range(num_students_one, num_students_one + num_students_two)

	# return student_ids_one, student_ids_two

def are_unique(l1, l2):
	return (set(l1).intersection(set(l2)) == set([]))

if __name__ == "__main__":
	types_and_sizes = [("MBA", 39), ("MEng", 35)]
	l1 = [2, 3]
	l2 = [2, 1, 6, 7]
	print are_unique(l1, l2)
