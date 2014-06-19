#import exceptions
import random

class InputError(Exception):
	def __init__(self, value):
		self.val = value
	def __str__(self):
		return repr(self.val)

class FunctionError(Exception):
	def __init__(self, value):
		self.val = value
	def __str__(self):
		return repr(self.val)

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
	# TODO: must guarantee that each team has at least one player of each team.
	# PSEUDOCODE
	# if student ID lists are empty or team sizes is empty, error.
	# if the lists are not unique, error.
	# make a list of length toReturn = (total students / team_size) (also integer division is a thing YAY)
	# while there are still teams to make (for i in range (0, toReturn))
	# 	make a temporary team team_creating of [None] * team_size
	#	team_index = 0
	# 	num_left = team_size
	# 	while num_left > 0
	#		cur_team = None
	# 		generate a random number between 0 and 1.
	#		if the number is greater than 0.5, cur_team is the MBA team.
	#		otherwise, cur_team is the MEng team. (check for errors here)
	#		generate a random integer r between 0 and len(cur_team)
	#		cur_student_id = cur_team.pop(r) (this is good because it actually removes the ID
	# 							from the original list)
	#		team_creating[team_index] = cur_student_id
	#		team_index += 1
	# 		num_left -= 1
	#	toReturn[i] = team_creating
	# print out the leftover students (iterate through both lists and print IDs)

	if ((MBA_student_ids == []) | (MEng_student_ids == [])):
		raise InputError('Student ID lists must not be empty.')
	elif (not are_unique(MBA_student_ids, MEng_student_ids)):
		raise InputError('Student ID lists must not overlap.')
	else:
		total_students = len(MBA_student_ids) + len(MEng_student_ids)
		num_teams = total_students / team_size
		to_return = [None] * num_teams
		for i in range(0, num_teams):
			team_creating = [None] * team_size
			team_index = 0
			num_left = team_size
			while (num_left > 0):
				cur_team_info = None
				rand = random.random()
				
				# Choosing which team to take a student from.
				if (rand >= 0.5 and not(MBA_student_ids == [])):
					cur_team_info = ("MBA", MBA_student_ids)
				elif (not (MEng_student_ids == [])):
					cur_team_info = ("MEng", MEng_student_ids)
				else:
					raise FunctionError('AMEYA FIX THIS: Both teams are empty.')
				
				# Choose which player to take from the current team.
				if (cur_team_info == None):
					raise FunctionError('AMEYA FIX THIS: Cur team not assigned.')
				else:
					cur_team_name = cur_team_info[0]
					cur_team = cur_team_info[1]
				
				if (len(cur_team) == 1):
					r = 0
				else:
					r = random.randint(0, len(cur_team) - 1)
				
				# Place the player onto our current team.
				cur_student_id = cur_team.pop(r)
				to_add = (cur_team_name, cur_student_id)
				team_creating[team_index] = to_add
				team_index += 1
				num_left -= 1

			to_return[i] = team_creating
		print to_return
		print "MEng student IDs is "
		print MEng_student_ids
		print "MBA student IDs is "
		print MBA_student_ids


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
	#types_and_sizes = [("MBA", 39), ("MEng", 35)]
	l1 = [3]
	l2 = [2, 1, 6, 7]
	create_teams(l1, l2, 3)
