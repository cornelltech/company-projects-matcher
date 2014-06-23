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

					TODO: add to teams based on their technical/businessy needs.

		Returns
		--------
		A tuple (teams, l1, l2, team_size), with:

			teams: a list of lists that represent teams. Each team list will contain 
			(type * id) tuples.

			l1: the first team passed into create_teams.

			l2: the second team passed into create_teams.

			team_size: passed along from input.

	'''
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
		to_return = [None] * (num_teams + 1)
		
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
				cur_student_id = cur_team.pop(r)
				to_add = (cur_team_name, cur_student_id)
				team_creating[team_index] = to_add
				team_index += 1
				num_left -= 1

			to_return[i] = team_creating

		to_return[num_teams] = [None] * team_size

		print "After running create_teams:"
		print "     MEng student IDs is: " + str(MEng_student_ids)
		print "     MBA student IDs is: " + str(MBA_student_ids)

		print "     Initial solution space is: " + str(to_return)

		return (to_return, MBA_student_ids, MEng_student_ids, team_size)

# TODO: undefined size thing. Look at TODOs above create_teams.

def teams_with_empty_spots(output):
	'''
		A list of the same size as our num_teams, which contains a 1 at spot i if
		the i-th team has spots for new members.
	'''
	result = [0] * len(output)
	cur = 0
	for team in output:
		for spot in team:
			if (spot == None):
				result[cur] += 1
		cur += 1
	return result

def add_students_to_team(remaining_students, s_type, output, empty_spots):
	'''
		Given remaining students (and type), an output from create_teams, and
		a list of empty spots in the list (comes from teams_with_empty_spots):
		add the remaining students to teams with spots.
	'''
	team_to_look_at = 0 
	if (len(remaining_students) == 0):
		return output

	while (len(remaining_students) > 0):
			
	# Get a random student
		if (len(remaining_students) == 1):
			r = 0
		else:
			r = random.randint(0, len(remaining_students) - 1)

		cur_student_id = remaining_students.pop(r)
		new_student = (s_type, cur_student_id)
		
		# Find the next available spot.

		# TODO: decide what to do in the case where there is no existing team to look at.
		#  		could add one extra team of all None as a buffer to the initial. Would never
		# 		need more than 1 such buffer because if there was room for one more team,
		# 		it would have already been made.
		while (empty_spots[team_to_look_at] <= 0):
		 	team_to_look_at += 1
		 	if (team_to_look_at > (len(output) - 1)):
		 		print "Ended early. Output is: ",
		 		print output
				return output
		
		cur_team = output[team_to_look_at]

		# We have found a team with an empty spot.
		for i in range (0, len(cur_team)):
			if (cur_team[i] == None):
				cur_team[i] = new_student
				break
		
		# Update the empty spots structure.
		empty_spots[team_to_look_at] -= 1
	
	print "After adding extra students to teams, our solution space is ",
	print output

	return output


# TODO: ensure that the teams satisfy the three criteria specified in 
# 		create_teams (i.e. one of each type of student on each team.)
#		Can do this by checking how many of each type there are
# 		on each team, and 
def fill_teams(all_output):
	'''
		Used after the initial loop assigning students to teams. Used to assign remaining
		students to teams.

		Parameters
		----------
		output: the team formations that create_teams will output.

	'''
	output_solution = all_output[0]
	remaining_MBAs = all_output[1]
	remaining_MEngs = all_output[2]

	has_spots = teams_with_empty_spots(output_solution)

	# Random number to determine which students to add to team first.
	rand = random.random()
	if (rand >= 0.5):
		add_students_to_team(remaining_MEngs, 'MEng', output_solution, has_spots)
		add_students_to_team(remaining_MBAs, 'MBA', output_solution, has_spots)
	else:
		add_students_to_team(remaining_MBAs, 'MBA', output_solution, has_spots)
		add_students_to_team(remaining_MEngs, 'MEng', output_solution, has_spots)

	#print "Diversity: " + str(is_diverse(output_solution))

	#if (not (is_diverse(all_output))):
	#	print "Not diverse"
	#	return output_solution 
		# TODO: add some swaps to make it diverse.		
	#else:
		return output_solution

def get_diversity_stats(all_output):
	count = 0
	output = all_output[0]
	result = [None] * len(output)
	for team in output:
		MBA_count = 0
		MEng_count = 0
		for person in team:
			# print "Person is " + str(person)
			if (person != None):
				if (person[0] == "MBA"):
					MBA_count += 1
				elif (person[0] == "MEng"):
					MEng_count += 1
		result[count] = (MBA_count, MEng_count)
		count += 1
	return result

# def find_problematic_teams(output):
# 	result = [(None, None)] * len(output)
# 	for team in output:
# 		MBA_count = 0
# 		MEng_count = 0
# 		# TODO: this is not a boolean anymore
# 		if (not (is_diverse_team(team))):
# 			for person in team:




# def make_diverse(output):
# 	for team in output:



def clean_team(all_output):
	output = all_output[0]
	result = [None] * len(output)
	cur = 0
	for team in output:
		filtered_team = [tup for tup in team if tup != None]
		result[cur] = filtered_team
		cur += 1
	return [r for r in result if r != None]

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
	o = create_teams(l1, l2, 5)
	fill_teams(o)
	#print is_diverse(o)

	print get_diversity_stats(o)

	# res = have_spots(output)
	# print res

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



