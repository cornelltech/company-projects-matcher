import random
import math
import ConfigParser

# TODO: move these to a globals file.
'''To ensure that we do not create multiple students, teams, or projects with the same ID.'''

configParser = ConfigParser.ConfigParser()
configFilePath = r'config.txt'
configParser.read(configFilePath)

# Declaring valid values for all fields.
vals_cs_ug = [True, False]
max_work_experience = configParser.getint('valid_values', 'max_work_experience')
vals_work_experience = range(0, max_work_experience+1)

# 0 = lowest, 4 = most
max_coding_ability = configParser.getint('valid_values', 'max_coding_ability')
vals_coding_ability = range(0, max_coding_ability+1)

# Keep these organized in alphabetical order. 
# NOTE: fix this.
vals_degree_pursuing = { 0 : "MBA", 1 : "MEng"}

# Valid IDs for our projects.
num_valid_projects = configParser.getint('valid_values', 'num_valid_projects')
vals_valid_projects = map(lambda x: x * 65, range(16, 16 + num_valid_projects))

# TODO: remove these.
degree_weight = 0.25
cs_ug_weight = 0.25
coding_ability_weight = 0.25
work_experience_weight = 0.25

# TODO: should change this to 10 when I'm testing.
number_project_rankings = configParser.getint('valid_values', 'number_project_rankings')

existing_student_IDs = []
existing_team_IDs = []
existing_project_IDs = []

class FieldError(Exception):
	def __init__(self, value):
		self.val = value
	def __str__(self):
		return repr(self.val)

class CompError(Exception):
	def __init__(self, value):
		self.val = value
	def __str__(self):
		return repr(self.val)

class Student(object):

	global vals_cs_ug
	global vals_yrs_work_experience
	global vals_coding_ability
	global vals_valid_projects
	global number_project_rankings

	# Defining checks for setting properties.
	def check_valid(self, val, lst, s=""):
		if (not (val in lst)):
		 	error = "Invalid input " + str(val) + " for student " + str(self._ID) + " for field" + s + "."
		 	raise FieldError(error)
		else:
		 	pass

	def get_name(self):
		return self._name

	def set_name(self, val):
		self._name = val

	name = property(get_name, set_name, doc = "Get and set name.")

	def get_ID(self):
		return self._ID

	def set_ID(self, val):
		self._ID = val

	ID = property(get_ID, set_ID, doc = "Get and set student ID.")

	def get_degree_pursuing(self):
		return self._degree_pursuing

	def get_numer_degree_pursuing(self):
		if (self._degree_pursuing == 0 or self._degree_pursuing == 1):
			return self._degree_pursuing
		elif(self._degree_pursuing == "MBA"):
			return 0
		elif(self._degree_pursuing == "MEng"):
			return 1
		else:
			raise FieldError("What is this degree you're pursuing?")

	# NOTE: this sets the degree pursuing as  A STRING. NOT 0/1
	def set_degree_pursuing(self, val):
		# Checks if the user is passing in the string value for degree pursuing.
		# If not, check if the int they're passing in is included in our dict.
		if (not(val in vals_degree_pursuing.values())):
			self.check_valid(val, vals_degree_pursuing, 
						s = " degree pursuing")
			self._degree_pursuing = vals_degree_pursuing[val]
		# If they are, set the degree pursuing
		else:
			self._degree_pursuing = val

	degree_pursuing = property(get_degree_pursuing, set_degree_pursuing,
					doc = "Get and set degree pursuing.")

	def get_coding_ability(self):
		return self._coding_ability

	def set_coding_ability(self, val):
		self.check_valid(val, vals_coding_ability, s = " coding ability")
		self._coding_ability = val

	coding_ability = property(get_coding_ability, set_coding_ability,
					 doc = "Get and set coding ability.")

	def get_cs_ug(self):
		return self._was_cs_ug

	def set_cs_ug(self, val):
		self.check_valid(val, vals_cs_ug, s = " was cs undergrad")
		self._was_cs_ug = val

	was_cs_ug = property(get_cs_ug, set_cs_ug,
				doc = "Get and set if student was a CS undergrad.")

	def get_work_experience(self):
		return self._work_experience

	def set_work_experience(self, val):
		self.check_valid(val, vals_work_experience, s = " num yrs. work experience")
		self._work_experience = val

	work_experience = property(get_work_experience, set_work_experience,
					  doc = "Get and set the num. yrs. of work experience.")

	def get_project_rankings(self):
		return self._project_rankings

	def check_valid_project_rankings(self, val):
		# Because val is a list and we want to check if each of the projects 
		# has a valid ID
		try:
			if (not (len(val) == number_project_rankings)):
				error = "There must be " + str(number_project_rankings) + " project rankings."
				raise FieldError(error)
		except TypeError:
			raise FieldError("Project rankings must be inputted as a list.")

		past = []
		for elm in val:
			self.check_valid(elm, vals_valid_projects, s = " project ID")
			if (elm in past):
				raise FieldError("Current student ID is " + str(self._ID) + ". Each project can only be entered once.")
			past.append(elm)

	def set_project_rankings(self, val):
		self.check_valid_project_rankings(val)
		self._project_rankings = val

	project_rankings = property(get_project_rankings, set_project_rankings,
					  doc = "Get and set the project rankings.")

	def set_valid_properties(self, degree_pursuing, cod_abil, cs_ug, num_yrs_work_exp, project_lst):
		
		self.set_degree_pursuing(degree_pursuing)
		self.set_coding_ability(cod_abil)
		self.set_cs_ug(cs_ug)
		self.set_work_experience(num_yrs_work_exp)
		self.set_project_rankings(project_lst)

	def __init__ (self, name, ID, degree_pursuing, cs_ug, cod_abil, num_yrs_work_exp, project_rnks, is_normalized=False):
		''' 
			Parameters
			----------
			ca    = coding ability. Int from 0 to 4, inclusive.
			csug  = was cs undergrad. Boolean.
			nywe  = num. years of work experience. Int from 0 to 4 (4 = 4+).
			project_lst = an integer list size number_project_rankings. Ints are the project IDs. 
						  The position of the int determines what rank it is.

		'''
		self._name				 	  = name
		self._ID				 	  = ID
		
		if (not(is_normalized)):
			self.set_valid_properties(degree_pursuing, cod_abil, cs_ug, num_yrs_work_exp, project_rnks)

		# If the data is already normalized, then we don't want to check membership with the above lists. 
		else:
			self._degree_pursuing = degree_pursuing
			self._coding_ability = cod_abil
			self._was_cs_ug = cs_ug
			self._work_experience = num_yrs_work_exp
			self._project_rankings = project_rnks

	def get_student_properties(self):
		tup = []
		tup.append(self._name)
		tup.append(self._ID)
		tup.append(self._degree_pursuing)
		tup.append(self._was_cs_ug)
		tup.append(self._coding_ability)
		tup.append(self._work_experience)
		tup.append(self._project_rankings)
		return tup

	# Get the number that this student ranked this project. 
	def get_ranking(self, project_id): 
		try:
			rankings = (self._project_rankings).tolist()
			ind = rankings.index(project_id)
			return (ind + 1)
		except(ValueError):
			# Student did not rank this project.
			return 100

	# The comment on #16 refers to this.
	# def get_interest_from_interest(self, rank):
	#	return abs(10 - rank)

	# Curved function that I wrote to close #2.
	def get_interest_from_ranking(self, rank):
		if (not(rank <= number_project_rankings)):
			raise CompError("Rank is invalid.")
		a = 10 * rank
		return a * math.sqrt(a)

	# This is the function to use when we are actually calculating
	# the goodness of a match.
	def get_cost_from_ranking(self, rank):
		if (not(rank <= number_project_rankings)):
			return 1000000000000000
		else:
			return (rank * rank)

class Team(object):

	global degree_weight
	global cs_ug_weight
	global coding_ability_weight
	global work_experience_weight

	def __init__(self, student_list, ID=-1, project_ID = 0):
		for student in student_list:
			if (student.ID in existing_student_IDs):
				error = "Student ID " + str(student.ID) + " is already taken."
				raise FieldError(error)
		#if ((len(student_list) == 4) or (len(student_list) == 5)):
		self._members = student_list
		#else:
			#raise FieldError("Team size must be 4 or 5.")
		if (ID == -1):
			new_id = random.randint(0, 100000)
			while (new_id in existing_team_IDs):
				new_id = random.randint(0, 100000)
			self._ID = new_id
			existing_team_IDs.append(self._ID)
		else:
			if (ID in existing_team_IDs):
				error = "Team ID " + str(ID) + "is already taken."
				raise FieldError(error)
			else:
				self._ID = ID
				existing_team_IDs.append(self._ID)

		num_MBAs = len(filter(lambda x: x.degree_pursuing == 0, self._members))
		num_MEngs = len(filter(lambda x: x.degree_pursuing == 1, self._members))

		self._project_ID = project_ID
		self._num_MBAs = num_MBAs
		print "num_MBAs is " + str(self._num_MBAs)
		self._num_MEngs = num_MEngs
		print "num_MEngs is " + str(self._num_MEngs)

	def get_num_MBAs(self):
		return self._num_MBAs

	# TODO: change this.
	def set_num_MBAs(self, val):
		raise FieldError("In team, cannot set number of MBAs.")

	num_MBAs = property(get_num_MBAs, set_num_MBAs,
				  doc = "Get and set the number of MBAs that this team requires.")

	def get_num_MEngs(self):
		return self._num_MEngs

	# TODO: change this.
	def set_num_MEngs(self, val):
		raise FieldError("In team, cannot set number of MEngs.")

	num_MEngs = property(get_num_MEngs, set_num_MEngs,
				  doc = "Get and set the number of MEngs that this team requires.")

	def get_project_ID(self):
		return self._project_ID

	def set_project_ID(self, val):
		if (not(val in vals_valid_projects)):
			error = str(val) + " is not a valid project ID for team " + str(self._ID)
			raise FieldError(error)
		else:
			self._project_ID

	project_ID = property(get_project_ID, set_project_ID,
					  doc = "Get and set the team's project ID.")
	
	def get_ID(self):
		return self._ID

	def set_ID(self, val):
		if (not(val in existing_team_IDs)):
			self._ID = val
			existing_team_IDs.append(self._ID)
		else:
			raise FieldError("This Team ID is already taken.")

	ID = property(get_ID, set_ID,
					  doc = "Get and set the team's ID, if not in the existing IDs.")

	def get_members(self):
		return self._members

	def set_members(self, val):
		for student in val:
			if (student in existing_student_IDs):
				error = "Student ID " + str(student.ID) + " is already taken."
				raise FieldError(error)
		else:
			self._members = val
			for student in self._members:
				existing_student_IDs.append(student.ID)

	members = property(get_members, set_members, 
					   doc = "Get and set the team's members (list of Students).")

	def get_existing_team_IDs():
		return existing_team_IDs

	def print_team(self):
		for student in self._members:
			print student.get_student_properties()

	# TODO: move this from the Team class to somewhere it actually belongs.
	def avg_list(self, lst):
		return (sum(lst) * 1.0)/len(lst)

	def pretty_print_properties(self):

		print "**************************************************************************"
		print "Stats for team ",
		print str(self._ID) + " are :"
		print ""


		print "Degrees pursuing"
		print "-----------------"
		for student in self._members:
			print "Student " + str(student.ID) + ": ",
			print student.degree_pursuing
		print ""


		print "CS Undergrad?"
		print "-----------------"
		for student in self._members:
			print "Student " + str(student.ID) + ": ",
			print student.was_cs_ug
		print ""


		print "Coding ability"
		print "-----------------"
		for student in self._members:
			print "Student " + str(student.ID) + ": ",
			print student.coding_ability
		print ""

		print "Work experience"
		print "-----------------"
		for student in self._members:
			print "Student " + str(student.ID) + ": ",
			print student.work_experience
		print ""


		print "**************************************************************************"


	def calculate_technical_rating(self):
		degrees = [student.degree_pursuing for student in self._members]
		csugs = [student.was_cs_ug for student in self._members]
		coding_abilities = [student.coding_ability for student in self._members]
		work_experiences = [student.work_experience for student in self._members]

		degrees_avg = self.avg_list(degrees)
		csugs_avg = self.avg_list(csugs)
		coding_abilities_avg = self.avg_list(coding_abilities)
		work_experience_avg = self.avg_list(work_experiences)

		# Hack because these var names are too long to fit on one line...
		tech_rating_x = degree_weight*degrees_avg + cs_ug_weight*csugs_avg 
		tech_rating_y = coding_ability_weight*coding_abilities_avg
		tech_rating_z = work_experience_weight*work_experience_avg

		return tech_rating_x + tech_rating_y + tech_rating_z

	# Sub =  we should subtract the values from a pair of students
	# Not sub = we should just check if those values are different
	def calculate_pairwise_differences(self, lst, sub = True):
		ret = 0
		used_indices = []
		index_one = 0
		index_two = 0
		for mem_one in lst:
			for mem_two in lst:
				if (sub):
					diff = abs(mem_one - mem_two)
				else:
					if (mem_one == mem_two):
						diff = 0
					else:
						diff = 1
				tup_one = (index_one, index_two)
				tup_two = (index_two, index_one)
				if (tup_one in used_indices or tup_two in used_indices):
					pass
				else:
					ret += diff
					used_indices.append((index_one, index_two))
				index_two += 1
			index_one += 1
			index_two = 0
		return ret

	def calculate_all_pairwise_differences(self):
		degrees = [student.degree_pursuing for student in self._members]
		csugs = [student.was_cs_ug for student in self._members]
		coding_abilities = [student.coding_ability for student in self._members]
		work_experiences = [student.work_experience for student in self._members]

		print "Deg:",
		print degrees
		print "Csug:",
		print csugs
		print "Coding abilities:",
		print coding_abilities
		print "Work experience:",
		print work_experiences


		diff_degrees = self.calculate_pairwise_differences(degrees, False)
		diff_csugs = self.calculate_pairwise_differences(csugs, False)
		diff_coding_abilities = self.calculate_pairwise_differences(coding_abilities)
		diff_work_experiences = self.calculate_pairwise_differences(work_experiences)
		
		return [diff_degrees, diff_csugs, diff_coding_abilities, diff_work_experiences]


	def do_diversity_calculation(self):
		pairwise_differences = self.calculate_all_pairwise_differences()
		print "Pairwise differences is",
		print pairwise_differences
		
		normal_avg = self.avg_list(pairwise_differences)

		degree_weight = 0.5
		csug_weight = 0.1
		coding_weight = 0.3
		work_weight = 0.1

		deg = (pairwise_differences[0] * 1.0)
		cs = (pairwise_differences[1] * 1.0)
		cod = (pairwise_differences[2] * 1.0)
		work = (pairwise_differences[3] * 1.0)

		weighted_avg = degree_weight*deg + coding_weight*cod + csug_weight*cs + work_weight*work

		print "Normal avg is",
		print normal_avg
		print "Weighted avg is",
		print weighted_avg
		print "Average on a scale of 0 to 1 is",
		print weighted_avg/4
		print "Going to return weighted average."

		return weighted_avg


	def calculate_interest_rating(self, project_id):
		rankings = [student.get_ranking(project_id) for student in self._members]
		interests = []
		for i in range(0, len(rankings)):
			cur_interest = self._members[i].get_interest_from_ranking(rankings[i])
			interests.append(cur_interest)	

		normalized_interests = self.normalize_bet_zero_and_one(interests)
		avg_interests = self.avg_list(normalized_interests)
		return avg_interests

	def normalize_bet_zero_and_one(self, lst):

		lst_max = max (lst)
		lst_min = min (lst)
		den = lst_max - lst_min
		num = [elm - lst_min for elm in lst]
		if (den == 0):
			raise CompError("In normalizing our quantitative variables, all values are the same.")
		final = [(elm * 1.0) / den for elm in num]
		return final

	def val_objective_function(self):
		# tech_rating = self.calculate_technical_rating()
		pass

class Project(object):
	def __init__(self, ID, num_MBAs, num_MEngs):
		self.set_ID(ID)
		self.set_num_MBAs(num_MBAs)
		self.set_num_MEngs(num_MEngs)
		self._remaining_MBA_spots = num_MBAs
		self._remaining_MEng_spots = num_MEngs
		self._students = []
		self._MBA_list  = []
		self._MEng_list = []
		# Waiting students is meant to be tuples of (rank, student) form.
		# I.e. (2, ameya)  means that ameya ranked this project 2 and is waiting.
		self._waiting_students = []

	def check_valid_student_nums(self, num_students):
		try:
			if(num_students < 0):
				error = "Number of required MBAs and MEngs must be positive."
				raise FieldError(error)
		except(TypeError):
			error = "Number of required MBAs and MEngs must be integers."
			raise FieldError(error)

	def get_ID(self):
		return self._ID

	def set_ID(self, val):
		if (val in existing_project_IDs):
			error = "ID " + str(val) + " is already taken."
			raise FieldError(error)
		elif(not(val in vals_valid_projects)):
			error = "ID " + str(val) + " is not valid."
			raise FieldError(error)
		else:
			self._ID = val
			existing_project_IDs.append(val)

	ID = property(get_ID, set_ID,
				  doc = "Get and set the team's ID, if not in the existing IDs.")

	def get_num_MBAs(self):
		return self._num_MBAs

	def set_num_MBAs(self, val):
		self.check_valid_student_nums(val)
		self._num_MBAs = val

	num_MBAs = property(get_num_MBAs, set_num_MBAs,
				  doc = "Get and set the number of MBAs that this team requires.")

	def get_num_MEngs(self):
		return self._num_MEngs

	def set_num_MEngs(self, val):
		self.check_valid_student_nums(val)
		self._num_MEngs = val

	num_MEngs = property(get_num_MEngs, set_num_MEngs,
				  doc = "Get and set the number of MEngs that this team requires.")

	def get_MEng_list(self):
		return self._MEng_list

	def set_MEng_list(self, val):
		error = "Cannot manually set the MEng list. Must add students via add_student function."
		raise FieldError(error)

	MEng_list = property(get_MEng_list, set_MEng_list,
				  doc = "Get and set the MEng list on this project.")

	def get_MBA_list(self):
		return self._MBA_list

	def set_MBA_list(self, val):
		error = "Cannot manually set the MBA list. Must add students via add_student function."
		raise FieldError(error)

	MBA_list = property(get_MBA_list, set_MBA_list,
				  doc = "Get and set the MBA list on this project.")

	def get_students(self):
		return self._students

	def set_students(self):
		error = "Cannot manually set the students list. Must add students via add_student function."
		raise FieldError(error)

	students = property(get_students, set_students, 
						doc = "Get and set the students on this project.")

	def get_waiting_students(self):
		return self._waiting_students

	def set_waiting_students(self, val):
		error = "Cannot manually set the waiting students list. Must add students via add_waiting_student function."
		raise FieldError(error)

	waiting_students = property(get_waiting_students, set_waiting_students, 
								doc = "Get and set the waiting students for this project. ")

	def get_remaining_MBA_spots(self):
		return self._remaining_MBA_spots

	def set_remaining_MBA_spots(self, val):
		error = "Cannot manually set the remaining MBA spots."
		raise FieldError(error)

	remaining_MBA_spots = property(get_remaining_MBA_spots, set_remaining_MBA_spots,
				  doc = "Get and set the remaining MBA spots on this project.")

	def get_remaining_MEng_spots(self):
		return self._remaining_MEng_spots

	def set_remaining_MEng_spots(self, val):
		error = "Cannot manually set the remaining MEng spots."
		raise FieldError(error)

	remaining_MEng_spots = property(get_remaining_MEng_spots, set_remaining_MEng_spots,
				  doc = "Get and set the remaining MEng spots on this project.")

	def has_remaining_MBA_spots(self):
		MBAs = filter(lambda s: s.degree_pursuing == 0 or s.degree_pursuing == "MBA", self._students)
		num_MBAs_needed = self._num_MBAs - len(MBAs)
		return (num_MBAs_needed > 0)

	def has_remaining_MEng_spots(self):
		MEngs = filter(lambda s: s.degree_pursuing == 1 or s.degree_pursuing == "MEng", self._students)
		num_MEngs_needed = self._num_MEngs - len(MEngs)
		return (num_MEngs_needed > 0)

	def has_remaining_spots(self):
		return self.has_remaining_MBA_spots() or self.has_remaining_MEng_spots()
 
	def has_waiting_students(self):
		return (len(self.waiting_students) > 0)

	# TODO: Add a way to check that ID doesnt exist on another team.
	# ^^^^ actually don't want that because at some intermediate point, we might want the same student
	# two different projects.
	def add_student_to_MBAs(self, student, verbose = False):
		if (not(student.degree_pursuing == 0 or student.degree_pursuing == "MBA")):
			if (verbose):
				print "Degree is not 0 or MBA"
			return False
		elif (not(self.has_remaining_MBA_spots())):
			if (verbose):
				print "This project does not have remaining MBA spots"
			return False
		else:
			MBA_IDs  = [s.ID for s in self._MBA_list]
			if (student.ID in MBA_IDs):
				if (verbose):
					print "Student is already on team"
				return False
				#error = "ID " + str(student.ID) + " is already on project " + str(self._ID) + "."
				#raise FieldError(error)
		self._MBA_list.append(student)
		self._students.append(student)
		self._remaining_MBA_spots -= 1
		return True

	# NOTE: returns a boolean!!!!
	def add_student_to_MEngs(self, student):
		if (not(student.degree_pursuing == 1 or student.degree_pursuing == "MEng")):
			return False
		elif (not(self.has_remaining_MEng_spots())):
			return False
		else:
			MEng_IDs  = [s.ID for s in self._MEng_list]
			if (student.ID in MEng_IDs):
				return False
				#error = "ID " + str(student.ID) + " is already on project " + str(self._ID) + "."
				#raise FieldError(error)
		self._MEng_list.append(student)
		self._students.append(student)
		self._remaining_MEng_spots -= 1
		return True

	# Returns a boolean of if the add was successful or not.
	def add_student(self, student, verbose = False):
		if (student.degree_pursuing == "MBA" or student.degree_pursuing == 0):
			if (verbose):
				print "Adding an MBA. ID is " + str(student.ID)
			return self.add_student_to_MBAs(student, verbose)
		elif (student.degree_pursuing == "MEng" or student.degree_pursuing == 1):
			if (verbose):
				print "Adding an MEng. ID is " + str(student.ID)
			return self.add_student_to_MEngs(student)
		else:
			raise FieldError("Are there more than two types?")

	def has_spot_for_one_more(self):
		return (len(self.students) <= 4)

	def num_spots_remaining(self):
		return self._remaining_MEng_spots + self._remaining_MBA_spots

	def add_waiting_student(self, student, verbose = False):
		if (student in self._MBA_list or student in self._MEng_list):
			# error = "Student " + str(student.ID) + " is already on project " + str(self._ID)
			# raise FieldError(error)
			pass
		else:
			# deg = student.degree_pursuing
			# if ((deg == "MBA" or deg == 0)):
			# 	value = self.add_student_to_MBAs(student)
			# 	if (verbose):
			# 		print value
			# elif ((deg == "MEng" or deg == 1) and self.has_remaining_MEng_spots()):
			# 	value = self.add_student_to_MEngs(student)
			# 	if (verbose):
			# 		print value
			# else:
			
			# Get the rank that this student gave this project.
			rank = student.get_ranking(self._ID)
			# Create a tuple of the project ranking and the student.
			tup = (rank, student)
			# Add the tuple to the waiting students list.
			self._waiting_students.append(tup)

	def is_empty(self):
		return (self._remaining_MEng_spots == self._num_MEngs and self.remaining_MBA_spots == self._num_MBAs)

	def add_team(self, team):
		# Check if team is an appropriate fit for the project.
		if (not(team.num_MBAs == self._num_MBAs and team.num_MEngs == self._num_MEngs)):
			error = "Team specs are (" + str(team.num_MBAs) + ", " + str(team.num_MEngs) + "). "
			error_two = "Project specs are (" + str(self._num_MBAs) + ", " + str(self._num_MEngs) + ")."
			raise FieldError("Team specs do not match project specs. " + error + error_two)
		elif (self.is_empty()):
			for student in team.members:
				self.add_student(student)
		else:
			raise FieldError("There are already members on this project. Would you like to proceed and erase these members?")

	def print_project_members(self):
		if (not (self._MEng_list == [] and self._MBA_list == [])):
				print ""
				print "For project " + str(self._ID) + ":"
				print "MEngs:",
				for stud in self._MEng_list:
					print stud.get_student_properties()
				if (len(self._MEng_list) == 0):
					print "None"
				print "MBAs:",
				for stud in self._MBA_list:
					print stud.get_student_properties()
				if (len(self._MBA_list) == 0):
					print "None"
				print ""
		else:
			print "None"

	def create_team_from_project(self):
		student_list = self._MBA_list + self._MEng_list
		print "Project ID " + str(self._ID)
		print "Length of student list is " + str(len(student_list))
		for s in student_list:
			print s.get_student_properties()
		if (not(len(student_list) == 4)):
			return
		t = Team(student_list, project_ID = self._ID)
		return t
		# project: def __init__(self, ID, num_MBAs, num_MEngs):
		# team:  def __init__(self, student_list, ID=-1, project_ID = 0):

	def remove_student_from_project(self, student_ID):
		student_list = self._MBA_list + self._MEng_list
		student_IDs = [s.ID for s in student_list]
		if (not (student_ID in student_IDs)):
			# error = "Student " + str(student_ID) + " is not on project "
			# error_two = str(self._ID) + "."
			# raise CompError(error + error_two)
			pass
		else:
			# list of the student who has this ID 
			# TODO: unstable because the list will only have one element.
			matching_ID_lst = filter(lambda x: x.ID == student_ID, student_list)
			matching_student = matching_ID_lst[0]
			if (matching_student.degree_pursuing == 0):
				self._MBA_list.remove(matching_student)
			elif (matching_student.degree_pursuing == 1):
				self._MEng_list.remove(matching_student)
			else:
				raise FieldError("Are there more than two degrees pursuing?")

	# num: should we print the project number?
	def print_student_IDs(self, num = True, name = False, dct = ""):
		lst = []
	 	students = self._MBA_list + self._MEng_list
	 	if (len(students) > 0):
	 		if (num):
	 			print "Project " + str(self._ID) + ":"
	 		else:
	 			print dct[self._ID] + " project:"
	 		if (not(name)):
	 			for s in students:
	 				print s.ID,
	 			print""
	 		else:
	 			for s in students:
	 				print s.name,
	 				if (s.degree_pursuing == 0):
	 					deg = "MBA"
	 				else:
	 					deg = "MEng"
	 				msg = "(Degree: " + deg + ", "
	 				msg += "rank: " + str(s.get_ranking(self._ID) + 1) + ")"
					lst.append(s.get_ranking(self._ID))
	 				print msg
	 		lst = [1.0 * (elm + 1) for elm in lst]
	 		print "On average, students got their",
	 		print str(sum(lst) / len(lst)) + " pick."
	 		print ""


