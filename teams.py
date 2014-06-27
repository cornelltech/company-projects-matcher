#import exceptions
import random
from student import Student

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

used_IDs = []

# TODO: Make this work for arbitrary number of student types. 
# 		Can apply these (functions that apply to two teams) apply to 
#		three or more teams by taking input in a list, and then
# 		using map.
# TODO: Make this work with more than one team size.

def random_index(lst_length):
	if (lst_length == 1):
		r = 0
	else:
		r = random.randint(0, lst_length - 1)
	return r

def create_teams_on_all_fields(first_students, first_name, second_students, second_name, team_size):
	'''
		A loop that goes through the sample space of students
		and creates teams of students.

		The set of teams teams adhere to our requirements:
			- Plausibility: teams will be formed from selection without 
			replacement (each student is assigned to exactly one team.)
			- Size: Each team will be of a size found in team_sizes (or +- 1).
			- Diversity: each team will have one student of each input type.

		Parameters
		----------

		first_ids: a list of the student IDs of the first group of students
				   (i.e. MBAs).

		second_ids: a list of the student IDs of the second group of students
					(i.e. MEngs).

		team_size: the target size for teams. If there are extra students left
					at the end, we will add them to teams.
					This process will create 
						((total_num_students) mod team_size)
					teams with (team_size + 1) students.

		Returns
		--------
		A tuple (teams, l1, l2), with:

			teams: a list of lists that represents the current teams. Each team list will
			contain (type * id) tuples. These teams will also contain None.

			l1: the remaining members of the first group passed into create_teams_type_id.

			l2: the remaining members of the second group passed into create_teams_type_id.

	'''

	# print "Initial size of teams is "
	# print len(first_ids),
	# print "and "
	# print len(second_ids)

	# Guarantee proper input.
	if ((first_students == []) | (second_students == [])):
		raise InputError('Student lists must not be empty.')

	else:

		first_student_ids = [student.ID for student in first_students]
		second_student_ids = [student.ID for student in second_students]

		if (not are_unique(first_student_ids, second_student_ids)):
			raise InputError('Student ID lists must not overlap.')

		elif (team_size == 0):
			raise InputError('Team size cannot be zero.')
	
		else:
			total_students = len(first_students) + len(second_students)
			num_teams = total_students / team_size
			num_teams_left = num_teams
			# print "Num teams is " + str(num_teams)

			if (num_teams == 0):
				raise InputError('Team size is too large for given input.')

			if ((len(first_students) < num_teams) | (len(second_students) < num_teams)):
				raise InputError('Not enough members to produce balanced teams.')

			# Initialize empty array to hold the final teams.
			to_return = [None] * (num_teams + 1)
			
			# For each team that we need to create:
			for i in range(0, num_teams):
				
				# Initialize empty tuple to hold the current team.
				team_creating = [None] * (team_size + 1)
				
				# At the beginning, the team has neither MBAs nor MEngs.
				team_has_first = False
				team_has_second = False
				
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
							# Pick firsts first, if there are enough remaining.
							if (len(first_students) >= num_teams_left):
							#if (not (first_ids == [])):
								return (first_name, first_students)
							# Pick secondss otherwise.
							else:
								return (second_name, second_students)
						else:
							# Pick seconds first, if there are enough remaining.
							if (len(second_students) >= num_teams_left):
							#if (not (second_ids == [])):
								return (second_name, second_students)
							# Pick firsts otherwise.
							else:
								return (first_name, first_students)

					# Logic to pick the current team to take students from.
					def pick_cur_team():

						# If the team either has both first and second students
						# or the team has neither, we can pick the team in
						# a purely random manner through rand_team_choose().
						if (team_has_first == team_has_second):
							return rand_team_choose()

						# Otherwise, if the team doesn't have a first student,
						# we will add an first student.
						elif (not(team_has_first)):
							return (first_name, first_students)
						
						# Doesn't have second, so add second.
						else:
							return (second_name, second_students)

					# Call the above function.
					cur_team_info = pick_cur_team()

					# Extract fields.
					cur_team_name = cur_team_info[0]
					cur_team_students = cur_team_info[1]

					if (cur_team_name == first_name):
						team_has_first = True

					elif (cur_team_name == second_name):
						team_has_second = True

					# Sanity check for when we add more student types.
					else:
						raise FunctionError('Are there more than two types of students?')
					
					r = random_index(len(cur_team_students))
					
					# Place the player onto our current team.
					cur_student = cur_team_students.pop(r)
					to_add = cur_student
					team_creating[team_index] = to_add
					team_index += 1
					num_left -= 1

				to_return[i] = team_creating
				num_teams_left -= 1

			to_return[num_teams] = [None] * team_size

			# print "After running create_teams_type_id:"
			# print "     Second student IDs is: " + str(second_ids)
			# print "     First student IDs is: " + str(first_ids)

			# print "     Initial solution space is: " + str(to_return)

			return (to_return, first_students, second_students)

def random_student_ID():
	r = random.randint(0, 1000000)
	if (not (r in used_IDs)):
		used_IDs.append(r)
		return r
	else:
		random_student_ID()

def random_degree_pursuing():
	return random.randint(0, 1)

def random_coding_ability():
	return random.randint(0, 4)

def random_cs_ug():
	return random.randint(0, 1)

def random_type_technical_strength():
	return random.randint(1, 9)

def random_yrs_work_experience():
	return random.randint(0, 6)

def create_random_student(d = -1):
	'''
		Given the numbers of students in each group, generate random fields
		for each.
	
	'''
	# def __init__ (self, name, ID, degree_pursuing, cod_abil, cs_ug, type_tech_stren, num_yrs_work_exp):

	i = random_student_ID()
	if (d == -1):
		d = random_degree_pursuing()
	c = random_coding_ability()
	cs = random_cs_ug()
	t = random_type_technical_strength()
	n = random_yrs_work_experience()

	name = "Test"

	s = Student(name, i, d, c, cs, t, n)
	return s

	# first_ids = range(0, first_num)
	# i = 1000
	# # To ensure there is no overlap between the two sets of IDs that we create
	# while (i <= first_num):
	# 	i *= 10
	# second_ids = range (1, second_num+1) # To ensure zero isn't included in both
	# second_ids = [elm * i for elm in second_ids]
	# return (first_ids, second_ids)

def print_student_stats(a):
	try:
		print "(",
		print '"' + a.name + '",', 
		print str(a.ID) + ",",
		print str(a.degree_pursuing) + ",",
		print str(a.coding_ability) + ",",
		print str(a.was_cs_ug) + ",",
		print str(a.type_technical_strength) + ",",
		print str(a.work_experience) + ")"
	except AttributeError:
		error = "Passed a " + str(type(a)) + " to a function that expects a Student."
		raise FunctionError(error)

def create_random_students(n, d = -1):
	result = []
	for i in range(0, n):
		# print "Student " + str(i+1) + " is:"
		s = create_random_student(d)
		#print_student_stats(s)
		result.append(s)
	return result

def create_random_MBAs(n):
	return create_random_students(n, d = 0)

def create_random_MEngs(n):
	return create_random_students(n, d = 1)

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

def add_students_to_team_on_all_fields(remaining_students, s_type, output, empty_spots):
	'''
		Given remaining students (and type), an output from create_teams_type_id, and
		a list of empty spots in the list (comes from teams_with_empty_spots):
		add the remaining students to teams with spots.


		Parameters
		----------
		remaining_students: a list of ints (IDs of remaining students, who are all of the
							same type). "Remaining students" means that these students were
							not assigned to teams after create_teams_type_id. This list
							will be obtained from the second or third slot of the
							return tuple of create_teams_type_id.

		s_type: a string saying the type of the students in remaining_students.

		output: a list of int*string lists, which are assignments of students to teams
				(obtained from the first slot of the return tuple of create_teams_type_id).
				Note: these are not the students in remaining_students; the students in
				output have already been assigned to teams.

		empty_spots: a list of integers. If empty_spots[i] = 0, then the i-th team has no
					spots to add someone. If empty_spots[i] = n (>0), the i-th teams
					has n spots to add someone.

		Returns
		-------
		filled_teams: a list of int*string lists, which have the students from remaining_students
					  assigned to teams.

	'''

	team_to_look_at = 0 
	if (len(remaining_students) == 0):
		return output

	while (len(remaining_students) > 0):
			
	# Get a random student
		r = random_index(len(remaining_students))
	
		cur_student = remaining_students.pop(r)
		new_student = cur_student
		
		# Find the next available spot.
		while (empty_spots[team_to_look_at] <= 0):
		 	team_to_look_at += 1
		 	if (team_to_look_at > (len(output) - 1)):
		 		error = 'Add students to team ended early. Output is: ' + str(output)
		 		raise FunctionError(error)
		
		cur_team = output[team_to_look_at]

		# We have found a team with an empty spot.
		for i in range (0, len(cur_team)):
			if (cur_team[i] == None):
				cur_team[i] = new_student
				break
		
		# Update the empty spots structure.
		empty_spots[team_to_look_at] -= 1
	
	# print "After adding extra students to teams, our solution space is: "
	# print "     " + str(output)

	return output

def fill_teams_on_all_fields(all_output, first_name, second_name):
	'''
		Used after the initial loop assigning students to teams. Assigns remaining
		students to teams.

		Parameters
		----------
		all_output: the team formations that create_teams_type_id will output.
		
		first_name, second_name: names passed as inputs to create_teams_type_id.

		Returns
		-------
		fixed_output: A list of teams with the remaining students assigned to teams. 
					  The first_ids and second_ids lists from all_output are empty
					  after executing this function.

	'''
	output_solution = all_output[0]
	remaining_first_students = all_output[1]
	remaining_second_students = all_output[2]

	has_spots = teams_with_empty_spots(output_solution)

	# Random number to determine which students to add to team first.
	rand = random.random()
	if (rand >= 0.5):
		add_students_to_team_on_all_fields(remaining_second_students, second_name, output_solution, has_spots)
		add_students_to_team_on_all_fields(remaining_first_students, first_name, output_solution, has_spots)
	else:
		add_students_to_team_on_all_fields(remaining_first_students, first_name, output_solution, has_spots)
		add_students_to_team_on_all_fields(remaining_first_students, second_name, output_solution, has_spots)

	return output_solution

def get_student_type_diversity_all_fields(fixed_output, first_name, second_name):
	'''
		Sums up the type of each student in each team.

		Parameters
		----------
		N/A.

		Returns
		-------
		A tuple of lists, in the form (result, can_swap), where

			result: a list of int tuples, where result[i] = (num_a, num_b)
					indicates that the i-th team created has num_a members
					of student type 1 and num_b members of student type 2.

			can_swap: a list of boolean tuples, where can_swap[i] = (True, False)
					  means that the i-th team could spare at least 1 member of 
					  student type 1 but no members of student type 2. 

	'''
	count = 0
	result = [None] * len(fixed_output)
	can_swap = [[], []]
	
	# Filling up the result diversity list.
	for team in fixed_output:
		first_count = 0
		second_count = 0
		changed = False
		for student in team:
			# print "Person is " + str(person)
			if (student != None):
				if (student.degree_pursuing == first_name):
					first_count += 1
					changed = True
				elif (student.degree_pursuing == second_name):
					second_count += 1
					changed = True
		if (not changed):
			result[count] = (-1, -1)
		else:
			result[count] = (first_count, second_count)
		count += 1	

	# Filling up the can_swap list.
	i = 0
	for tup in result:
		if ((tup[0] >= 2) and (tup[1] >= 2)):
			can_swap[0].append(i)
			can_swap[1].append(i)
		elif (tup[0] >= 2):
			can_swap[0].append(i)
		elif (tup[1] >= 2):
			can_swap[1].append(i)
		else:
			pass
		i += 1

	# Result in the form (first_count, second_count)
	return (result, can_swap)

def is_type_diverse(fixed_output, first_name, second_name):
	'''
		Used after filling teams with the remaining students. Checks if the teams that
		were created are diverse, i.e. contains at least one of each type of student.

		Parameters
		----------
		fixed_output: the team formations that fill_teams_type_id will output.

		first_name, second_names: names passed as inputs to create_teams_type_id.

		Returns
		-------
		is_type_diverse: a boolean value indicating if the set of teams is diverse or not,
					as specified above.

	'''
	diversity_stats_output = get_student_type_diversity_all_fields(fixed_output, first_name, second_name)
	diversity_stats = diversity_stats_output[0]
	for tup in diversity_stats:
		if (0 in tup):
			return False
	return True

def clean_team(filled_teams):
	'''
		Removes the None values from teams after all remaining students
		have been assigned to teams.

		Parameters
		----------
		filled_teams: a list of lists with all students assigned to teams,
					  i.e. after running the fill_teams_type_id function.

		Returns
		-------
		clean_teams: a list of lists with all None values removed.

	'''
	result = [None] * len(filled_teams)
	cur = 0
	for team in filled_teams:
		filtered_team = [stud for stud in team if stud != None]
		result[cur] = filtered_team
		cur += 1
	return [r for r in result if r != None and r!= []] 

# TODO: implement pairwise differences, to ensure that teams are balanced.

# pseudocode for pairwise differences
# create a matrix of size (len(filled_teams) x len(filled_teams))
# If there are 3 teams, this would look like:
#    1 2 3
# 1  0 a b
# 2  a 0 c
# 3  b c 0
# my problems with a matrix for this info:
# 		- Redundant
# 		- Takes up more space
# Could do a list of lists with each list becoming smaller.

# Another option:
# 		- Only add the difference when its above one
# 		- Then tag it (for which teams it applies to)
# iterate through the list once (for team_1 in filled_teams)
# 	iterate again (for team_2 in filled_teams)
# 		if (team_1 == team_2): check if this is the proper equality check.
# 			pass
# 		else:
# 			len_1 = len(team_1)
# 			len_2 = len(team_2)
# 			diff = abs(len1 - len_2)
# 			add to the data structure
# 			

def get_pairwise_differences(filled_teams):
	raise FunctionError("get_pairwise_differences has not been implemented.")

def append_singles_to_other(cleaned_teams):
	for team in cleaned_teams:
		print "Team len is "
		print len(team)
		if (len(team) == 1):
			print "Hit the team length one case. Team is "
			print_student_list (team)
			print "The first team used to be "
			print_student_list (cleaned_teams[0])
			cleaned_teams[0].append(team[0])
			print "But now the first team is "
			print_student_list(cleaned_teams[0])
	return cleaned_teams

def fix_singletons_on_all_fields(fixed_teams, cleaned_teams, first_name, second_name):
	'''
		If there are teams with only one person, this will fix that problem.
		NOTE: currently finds a team that could spare a member of the desired type.
			  Creates a team of size 2.

		For example, if cleaned_teams is:

		Team 1: [('MBA', 3), ('MEng', 9), ('MBA', 12), ('MBA', 15), ('MEng', 18)]
		Team 2: [('MEng', 4)]

		Then, fix_singletons may return:

		Team 1: [('MEng', 9), ('MBA', 12), ('MBA', 15), ('MEng', 18)]
		Team 2: [('MEng', 4), ('MBA', 3)]

		Things.


	'''
	print "in fix singletons"
	print "fixed teams is "
	print_team_list(fixed_teams)



	def get_indices_of_singletons():
		i = 0
		result = []
		print "cleaned teams is "
		print_team_list (cleaned_teams)
		for team in cleaned_teams:
			print "Team len is "
			print len(team)
			if (len(team) == 1):
				result.append(team)
			i += 1
		return result

	lst = get_indices_of_singletons()
	print "The singleton list is "
	print lst

	if (len(lst) == 0):
		return cleaned_teams
	else:
	 	stats = get_student_type_diversity_all_fields(fixed_teams, first_name, second_name)
	 	can_swap = stats[1]
	 	can_swap_fst = can_swap[0]
	 	can_swap_snd = can_swap[1]
	 	for team in lst:
	 		first_member = team[0]
	 		team_name = first_member.degree_pursuing

	 		#print "Team is " + str(team)

	 		if (team_name == first_name):
	 			other_name = second_name
	 			swap_from = can_swap_snd
	 		elif (team_name == second_name):
	 			other_name = first_name
	 			swap_from = can_swap_fst
	 		else:
	 			# Sanity check
	 			raise FunctionError("Are there more than two types?")

			print "swap_from is:" + str(swap_from)
			if (len(swap_from) == 0):
				error = "There is no possible team to swap from. The existing teams are"
				error += str(fixed_teams)
				raise FunctionError(error)

			r = random_index(len(swap_from))
	 		# print "R is " + str(r)
	 		team_to_take_from = cleaned_teams[r]
	 		# print "Team to take from is " + str(team_to_take_from)

	 		#new = 0
	 		#cleaned_teams[index_of_singleton_team_in_teams].append(new)
	 		possible_members_to_swap = filter(lambda student: student.degree_pursuing == other_name, team_to_take_from)
	 		possible_indices = map(lambda member: team_to_take_from.index(member), possible_members_to_swap)

	 		# print "Possibilities is " + str(possible_members_to_swap)
	 		# print "Team is " + str(team)
	 		# print "Possible indices is " + str(possible_indices)

	 		print "len of possible indices is "
	 		print str(len(possible_indices))
	 		i = random_index(len(possible_indices))
	
	 		# print "i is " + str(i)

	 		index_to_swap_at = possible_indices[i]

	 		# print "index to swap at is " + str(index_to_swap_at)
	 		member_to_swap = team_to_take_from[index_to_swap_at]
	 		
	 		#print "member to swap is "
	 		#print member_to_swap.get_student_properties()
	 		# print "Member to swap is " + str(member_to_swap)

	 		#print "before append, team is "
	 		#print_student_list(team)

	 		team.append(member_to_swap)

	 		#print "after append, team is "
	 		#print_student_list(team)	
	 		# print "Team is now " + str(team)

	 		#print "team to take from is "
	 		#print_student_list(team_to_take_from)

	 		try:
	 			team_to_take_from.remove(member_to_swap)
	 			# print "Team to take from is now " + str(team_to_take_from)

	 		except ValueError:
	 			raise FunctionError("The member you are trying to remove is not in the given team.")

	 		
	 		print " TEAM LIST IS -----------------"
	 		print_team_list (cleaned_teams)

	 		return cleaned_teams
	 		
		# Then, go to a random of the indices and filter based on the desired name being part of the tuple.
		# Then, generate a random one of those.
		# Then, add that to the cleaned_team that is a singleton.

def are_unique(l1, l2):
	''' 
		Checks if two given lists are unique.

		Parameters
		----------
		l1, l2: two arbitrary lists.

		Returns
		-------
		are_unique: a boolean value indicating if these lists are unique.

	'''
	return (set(l1).intersection(set(l2)) == set([]))

def print_clean(solution_space):
	'''
		Formats printing teams.

		Parameters
		----------
		solution_space: a list of lists (obtained from clean_team).

		Returns
		-------
		None

	'''
	i = 1
	for team in solution_space:
		print "Team " + str(i) + ": ",
		print team
		i += 1

def print_team_list(lst_of_lsts):
	i = 1
	for lst in lst_of_lsts:
		if (not (lst == None)):
			print "Team " + str(i) + ":"
			print "-----"
			for student in lst:
				if (student != None):
					print student.get_student_properties(),
					print ", "
				else:
					print student
		print ""
		i += 1

def print_student_list(lst):
	for student in lst:
		print student.get_student_properties()

if __name__ == "__main__":
	pass



