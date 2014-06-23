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

		teams: a list of lists that represent teams. Each team list will contain 
		(type * id) tuples.

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

	# Guarantee proper input.
	if ((MBA_student_ids == []) | (MEng_student_ids == [])):
		raise InputError('Student ID lists must not be empty.')
	
	elif (not are_unique(MBA_student_ids, MEng_student_ids)):
		raise InputError('Student ID lists must not overlap.')

	elif (team_size == 0):
		raise InputError('Team size cannot be zero.')
	
	else:
		total_students = len(MBA_student_ids) + len(MEng_student_ids)
		num_teams = total_students / team_size

		if (num_teams == 0):
			raise InputError('Team size is too large for given input.')

		if ((len(MBA_student_ids) < num_teams) | (len(MEng_student_ids) < num_teams)):
			raise InputError('Not enough MBAs or MEngs to produce balanced teams.')

		# Initialize empty array to hold the final teams.
		to_return = [None] * num_teams
		
		# For each team that we need to create:
		for i in range(0, num_teams):
			
			# Initialize empty tuple to hold the current team.
			team_creating = [None] * (team_size + 1)
			
			# At the beginning, the team has neither MBAs nor MEngs.
			team_has_MBA = False
			team_has_MEng = False
			
			# Start adding to the beginning of the team.
			# Initially have the entire team to fill.
			team_index = 0
			num_left = team_size
			
			# While there are empty spots left on the team:
			while (num_left > 0):

				# Generate a random number between 0 and 1.
				rand = random.random()

				# Function to pick a team in a purely random manner.
				def rand_team_choose():
					if (rand >= 0.5):
						# Pick MBAs first, if not empty.
						if (not(MBA_student_ids == [])):
							return ("MBA", MBA_student_ids)
						# Pick MEngs if MBA is empty.
						else:
							return ("MEng", MEng_student_ids)
					else:
						# Pick MEngs first, if not empty.
						if (not(MEng_student_ids == [])):
							return ("MEng", MEng_student_ids)
						# Pick MBAs if MEng is empty.
						else:
							return ("MBA", MBA_student_ids)

				# Logic to pick the current team to take students from.
				def pick_cur_team():

					# If the team either has both MBA and MEng students
					# or the team has neither, we can pick the team in
					# a purely random manner through rand_team_choose().
					if (team_has_MBA == team_has_MEng):
						return rand_team_choose()

					# Otherwise, if the team doesn't have an MBA student,
					# we will add an MBA student.
					elif (not(team_has_MBA)):
						return ("MBA", MBA_student_ids)
					
					# Doesn't have MEng, so add MEng.
					else:
						return ("MEng", MEng_student_ids)

				# Call the above function.
				cur_team_info = pick_cur_team()

				# Extract fields.
				cur_team_name = cur_team_info[0]
				cur_team = cur_team_info[1]

				if (cur_team_name == "MBA"):
					team_has_MBA = True

				elif (cur_team_name == "MEng"):
					team_has_MEng = True

				# Sanity check for when we add more student types.
				else:
					raise FunctionError('Are there more than two types of students?')
				
				# Protect against randint error for team of size 1.
				if (len(cur_team) == 1):
					r = 0
				else:
					r = random.randint(0, len(cur_team) - 1)
				
				# Place the player onto our current team.
				# NOTE: if we want to keep the input teams unchanged, then change this
				# pop into a peek. The problem with this is that we will repeat the students
				# on the teams, and our loop will never end.
				cur_student_id = cur_team.pop(r)
				to_add = (cur_team_name, cur_student_id)
				team_creating[team_index] = to_add
				team_index += 1
				num_left -= 1

			to_return[i] = team_creating
		# NOTE: if we changed the above pop to a peek, printing this information
		# 		should be useless because our input teams should be unchanged.
		#		This would be a good place to sanity check for this.

		print "MEng student IDs is "
		print MEng_student_ids
		print "MBA student IDs is "
		print MBA_student_ids

		while (len(MEng_student_ids) > 0):
			r = random.randint(0, len(MEng_student_ids) - 1)
			cur_student_id = MEng_student_ids.pop(r)

		#NOTE: fill in None with the desired thingy.


		print to_return
		print "The formatted team is:",
		print_team (to_return)
		return to_return



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

def have_spots(output):
	'''
		The teams out of our result formation that have spots for new members.
	'''
	result = [0] * len(output)
	# print "length of result is "
	# print len(result)
	cur = 0
	# print "cur is "
	# print cur
	for team in output:
		for spot in team:
			if (spot == None):
				# print "spot is None"
				result[cur] = 1
		cur += 1
		# print "did iteration. cur is "
		# print cur
	return result

def fill_teams(t1, t1_type, t2, t2_type, team_size, res):
	'''
		Used after the initial loop assigning students to teams. Used to assign remaining
		students to teams.

		Parameters
		---------
		t1: team 1 (i.e. remaining MBA students.)

		t1_type: string telling us what type t1 is.

		t2: team 2 (i.e. remaining MEng students.)

		t2_type: string telling us what type t2 is.

		team_size: the ideal team size (taken from create_teams).

		res: the total team formations that create_teams will output.

	'''
	# while there are students left on t1
	while (len(t1) > 0):
		# get a random student
		if (len(t1) == 1):
			r = 0
		else:
			r = random.randint(0, len(t1) - 1)
		cur_student_id = t1.pop(r)
		res[team_size - 1] = (t1_type, cur_student_id)

# TODO: add in logic for commas in the right places.
def print_team(output):
	result = ""
	result += '['
	for team in output:
		result += '['
		for tup in team:
			if (tup != None):
				result += str(tup) + ' '
		result += ']'
	result += ']'
	print result

def are_unique(l1, l2):
	''' 
		Checks if two given lists are unique.
	'''
	return (set(l1).intersection(set(l2)) == set([]))

def do_loop_to_create_teams(t1, t2, s, n):
	'''
		A loop that runs create_teams n times on the given input
		lists t1 and t2. It will return a list of multiple random
		team formations from our input lists.

		Parameters:
		----------

		t1: a list of the student ids of the MBA students.

		t2: a list of the student ids of the MEng students.

		s: team_size (see create_teams docs.)

		n: number of iterations. 

		Returns:
		--------

		teams: a list of lists, where each internal list represents a team 
		formation and is therefore made up of (type * id) tuples.

	'''
	# TODO: copy the initial arrays over into a buffer.
	# TODO: create a while loop to perform the team creation multiple times.
	result = create_teams(t1, t2, s)
	return (t1, t2, result)

if __name__ == "__main__":
	#types_and_sizes = [("MBA", 39), ("MEng", 35)]
	l1 = [3, 19, 20, 8]
	l2 = [2, 1, 6, 7]

	# TODO: find out how to do assertion tests (or equivalent) in Python.

	# Checks for valid output

	# Use when above function is defined.
	# res = do_loop_to_create_teams(l1, l2, 3)
	# print "res is "
	# print res
	# t1 = res[0]
	# t2 = res[1]
	output = create_teams(l1, l2, 4)
	res = have_spots(output)
	print res

	# Checks for invalid input
	# create_teams(l1, l2, 0)
	# create_teams(l2, l1, 0)
	# create_teams([], [], 3)
	# create_teams([], [4], 1)
	# create_teams([], [4], 8)
	# create_teams([5], [], 1)
	# create_teams([5], [], 8)
	# create_teams([8], [9, 0], 4)
	# create_teams ([0], [8, 9], 4)



