import math
import ConfigParser
import distance
import itertools

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
vals_valid_projects = range(1, num_valid_projects+1)

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

	def check_valid_project_rankings(self, val, rankings_can_be_empty = False):
		# Because val is a list and we want to check if each of the projects 
		# has a valid ID
		try:
			if (len(val) == 0 and rankings_can_be_empty):
				self._project_rankings = val
			elif (not (len(val) == number_project_rankings)):
				error = "There must be " + str(number_project_rankings) + " project rankings."
				raise FieldError(error)
		except TypeError:
			raise FieldError("Project rankings must be inputted as a list.")

		past = []
		for elm in val:
			self.check_valid(elm, vals_valid_projects, s = " project ID")
			if (elm in past):
				raise FieldError("Student " + str(self._ID) + " entered project " + str(elm) + " twice.")
			past.append(elm)

	def set_project_rankings(self, val, rankings_can_be_empty = False):
		self.check_valid_project_rankings(val, rankings_can_be_empty)
		self._project_rankings = val

	project_rankings = property(get_project_rankings, set_project_rankings,
					  doc = "Get and set the project rankings.")

	def set_valid_properties(self, degree_pursuing, cod_abil, cs_ug, num_yrs_work_exp, 
							project_lst, rankings_can_be_empty = False):
		
		self.set_degree_pursuing(degree_pursuing)
		self.set_coding_ability(cod_abil)
		self.set_cs_ug(cs_ug)
		self.set_work_experience(num_yrs_work_exp)
		self.set_project_rankings(project_lst, rankings_can_be_empty)

	def __init__ (self, name, ID, degree_pursuing, cs_ug, cod_abil, num_yrs_work_exp, project_rnks, 
					is_normalized=False, rankings_can_be_empty = False):
		''' 
			Parameters
			----------
			ca    = coding ability. Int from 0 to 4, inclusive.
			csug  = was cs undergrad. Boolean.
			nywe  = num. years of work experience. Int from 0 to 4 (4 = 4+).
			project_lst = an integer list size number_project_rankings. Ints are the project IDs. 
						  The position of the int determines what rank it is.
			rankings_can_be_empty = The ranking list can be empty. This is so that we can construct students
									step by step. MIGHT REMOVE THIS.

		'''
		self._name				 	  = name
		self._ID				 	  = ID
		
		if (not(is_normalized)):
			self.set_valid_properties(degree_pursuing, cod_abil, cs_ug, 
										num_yrs_work_exp, project_rnks, rankings_can_be_empty)

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

	def get_numerical_student_properties(self):
		tup = []
		if (self._degree_pursuing == 0 or self._degree_pursuing == "MBA"):
			tup.append(0)
		elif (self._degree_pursuing == 1 or self._degree_pursuing == "MEng"):
			tup.append(1)
		else:
			raise ValueError("What is this degree pursuing?")
		tup.append(self._was_cs_ug)
		tup.append(self._coding_ability)
		tup.append(self._work_experience)
		return tup

	# Get the number that this student ranked this project. 
	# NOTE: returns 100 if the student did not rank the project.
	def get_ranking(self, project_id): 
		try:
			rankings = self._project_rankings.tolist()
			#print "Rankings is of type " + str(type(rankings))
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

	def set_students(self, students):
		self._students = students

		#error = "Cannot manually set the students list. Must add students via add_student function."
		#raise FieldError(error)

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

	# This just returns if the project strictly has remaining spots for MBAs.
	# Does not account for the wiggle room (+1 MEng OR +1 MBA).
	def has_remaining_MBA_spots(self):
		MBAs = filter(lambda s: s.degree_pursuing == 0 or s.degree_pursuing == "MBA", self._students)
		num_MBAs_needed = self._num_MBAs - len(MBAs)
		return (num_MBAs_needed > 0)

	# This just returns if the project strictly has remaining spots for MEngs.
	# Does not account for the wiggle room (+1 MEng OR +1 MBA).
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

	# This accounts for the wiggle room.
	def add_student_to_MBAs(self, student, wiggle, verbose = False):
		if (not(student._degree_pursuing == 0 or student._degree_pursuing == "MBA")):
			if (verbose):
				print "Degree is not 0 or MBA"
			return False
		elif (not(self.has_remaining_MBA_spots())):
			if (wiggle):
				if (len(self._students) > 4):
					if (verbose):
						print "This project does not have remaining MBA spots"
					return False
				# The wiggle spot is not taken. Can add this MBA.
				else: 
					self._MBA_list.append(student)
					self._students.append(student)
		else:
			MBA_IDs  = [s.ID for s in self._students if s.degree_pursuing == 0 or s.degree_pursuing == "MBA"]
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
	def add_student_to_MEngs(self, student, wiggle, verbose = False):
		if (not(student.degree_pursuing == 1 or student.degree_pursuing == "MEng")):
			if (verbose):
				print "Degree is not 1 or MEng"
			return False
		elif (not(self.has_remaining_MEng_spots())):
			if (wiggle):
			# Wiggle spot already taken
				if (len(self._students) > 4):
					if (verbose):
						print "This project does not have remaining Meng spots"
					return False
				# The wiggle spot is not taken. Can add this MEng.
				else: 
					self._MEng_list.append(student)
					self._students.append(student)
		else:
			MEng_IDs  = [s.ID for s in self._students if s.degree_pursuing == 1 or s.degree_pursuing == "MEng"]
			if (student.ID in MEng_IDs):
				return False
				#error = "ID " + str(student.ID) + " is already on project " + str(self._ID) + "."
				#raise FieldError(error)
			self._MEng_list.append(student)
			self._students.append(student)
			self._remaining_MEng_spots -= 1
			return True

	# Returns a boolean of if the add was successful or not.
	def add_student(self, student, wiggle, verbose = False):
		if (student.degree_pursuing == "MBA" or student.degree_pursuing == 0):
			if (verbose):
				print "Adding an MBA. ID is " + str(student.ID)
			return self.add_student_to_MBAs(student, wiggle, verbose)
		elif (student.degree_pursuing == "MEng" or student.degree_pursuing == 1):
			if (verbose):
				print "Adding an MEng. ID is " + str(student.ID)
			return self.add_student_to_MEngs(student, wiggle, verbose)
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

	def calculate_diversity(self, tup):
		#tup = distance.create_inv_cov_mat_from_data(use_file, students)
	#	print "In calculate diversity: tup is " + str(tup)
		inv_cov_mat = tup[0]
		dict_key_vals = tup[1]
	#	print "dict key vals is " + str(dict_key_vals)
		diversity = 0
		num_students = len(self._students)
		if (num_students < self.num_MBAs + self.num_MEngs):
			error = "Students on project " + str(self.ID) + " are " + str(self.students) + "."
			error += " This project is not full. Do you want to calculate diversity?"
			raise ValueError(error)
		else:
			attributes = []
			for student in self._students:
			#	print "student id is " + str(student.ID)
				#print "student id in dict_key_vals " + str()
			#	attributes.append("")
				attributes.append(dict_key_vals[student.ID])
			# Make a list of indices in attributes (using range)
			indices = range(len(attributes))

			# Generate all possible combinations of those (not permutations)
			pairs = itertools.combinations(indices, 2)
			for tup in pairs:
				fst = tup[0]
				snd = tup[1]
				fst_properties = attributes[fst]
				snd_properties = attributes[snd]
				d = distance.do_python_distance_data(fst_properties, snd_properties, inv_cov_mat)
				diversity += d

			# For all pairs in that:
			# Get attributes[first], attributes[second]
			# Calculate the diversity of these two lists
			# Add it to the diversity variable

	 	return diversity



