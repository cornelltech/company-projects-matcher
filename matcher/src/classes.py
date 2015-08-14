import ConfigParser
import distance
import itertools 
import numpy as np

configParser = ConfigParser.ConfigParser()
max_business_ability =None
vals_business_ability = None

max_work_experience = None
vals_work_experience = None

# 0 = lowest, 4 = most
max_coding_ability = None
vals_coding_ability = None

# Keep these organized in alphabetical order. 
vals_degree_pursuing = None

# Valid IDs for our projects.
num_valid_projects = None
vals_valid_projects = None

#duplicate projects for the 2 teams/project constraint
number_project_rankings = None
alg_number_project_rankings = None

duplicate_rankings = None

def init_classes(config):
        global max_business_ability
        global vals_business_ability
        global max_work_experience
        global vals_work_experience
        global max_coding_ability
        global vals_coding_ability
        global vals_degree_pursuing 
        global num_valid_projects 
        global vals_valid_projects 
        global number_project_rankings 
        global alg_number_project_rankings 
        global duplicate_rankings

        configFilePath = config.encode('string-escape')
        configParser.read(configFilePath)

        # Declaring valid values for all fields.
        try:
                max_business_ability = configParser.getint('valid_values', 'max_business_ability')
                vals_business_ability = range(0, max_business_ability+1)
        except (ConfigParser.Error):
                max_business_ability = 4
                vals_business_ability = range(0, max_business_ability+1)
        try:
                max_work_experience = configParser.getint('valid_values', 'max_work_experience')
                vals_work_experience = range(0, max_work_experience+1)
        except (ConfigParser.Error):
                max_work_experience = 4
                vals_work_experience = range(0, max_work_experience+1)
        # 0 = lowest, 4 = most
        try:
                max_coding_ability = configParser.getint('valid_values', 'max_coding_ability')
                vals_coding_ability = range(0, max_coding_ability+1)
        except (ConfigParser.Error):
                max_coding_ability = 4
                vals_coding_ability = range(0, max_coding_ability + 1)

        # Keep these organized in alphabetical order. 
        vals_degree_pursuing = { 0 : "MBA", 1 : "MEng", 2:"HT", 3:"CM"}

        # Valid IDs for our projects.
        try:
                num_valid_projects = configParser.getint('valid_values', 'num_valid_projects')
        except (ConfigParser.Error):
                num_valid_projects = 250

        #duplicate projects for the 2 teams/project constraint
        try:
                number_project_rankings = configParser.getint('valid_values', 'number_project_rankings')
                duplicate_rankings = configParser.getboolean('valid_values', 'duplicate_rankings')
                if duplicate_rankings:
                        alg_number_project_rankings = 2*number_project_rankings
                else:
                        alg_number_project_rankings = number_project_rankings
        except (ConfigParser.Error):
                number_project_rankings = 10
                duplicate_rankings = False
                alg_number_project_rankings = 10
        if duplicate_rankings:
                vals_valid_projects = range(1, (2*num_valid_projects) + 1)
        else :
                vals_valid_projects = range(1, num_valid_projects + 1)


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
        global alg_number_project_rankings
        global duplicate_rankings

	def __init__ (self, name, ID, degree_pursuing, bus_abil, cod_abil, num_yrs_work_exp,
				   project_rnks, bin_field = 0, is_normalized=False, rankings_can_be_empty = False):
		''' 
			Parameters
			----------
			name  = student's name (string).
			ID 	  = student's ID (int).
			degree_pursuing =  student's degree (string or int).
			    0 for MBA, 1 for MEng, 2 for HT, 3 for CM
			bus_abil  = student's business ability (int). From 0 to 4, inclusive.
			cod_abil  = student's coding ability (int). From 0 to 4, inclusive.
			num_yrs_work_exp  = student's years of professional work experience (int).
			    From 0 to 4, inclusive. 4 indicates 4 or more years of experience.
			project_rnks = a list of project IDs (int list).
			    Ints are the project IDs. There are number_project_rankings IDs.
			    Ranked in order of preference.
                        binary_field = any binary field you wish. Possible examples:
                           Local/not-local, male/female, was a CS undergrad/was not, etc. 
			is_normalized = indicates if values are normalized (bool).
			rankings_can_be_empty = indicates if the ranking list can be empty (bool).
			    (This allows us to construct students step by step.)

		    Returns
		    -------
		    Student object with given parameters as attributes.

		'''
                self._name = name
		self._ID = ID
		self.set_bin_field(bin_field)

		if (not(is_normalized)):
			self.set_valid_properties(degree_pursuing, cod_abil, bus_abil, 
										num_yrs_work_exp, project_rnks, rankings_can_be_empty)

		# If the data is already normalized, then we don't want to check membership with the above lists. 
		else:
			self._degree_pursuing = degree_pursuing
			self._coding_ability = cod_abil
			self._business_ability= bus_abil
			self._work_experience = num_yrs_work_exp
			self._project_rankings = np.asarray(list(itertools.chain.from_iterable((e,e+num_valid_projects) for e in project_rnks)))

	# Defining properties for Student attributes.
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

        def get_bin_field(self):
                return self.bin_field

        def set_bin_field(self, val):
                if not(val in [0,1]):
                        raise FieldError("Binary field must be either 0 or 1.")
                self._bin_field = val

        bin_field = property(get_name, set_name, doc = "Get and set the binary field.")

	def get_degree_pursuing(self):
		return self._degree_pursuing

	# NOTE: this sets the degree pursuing as a string, not 0 or 1.
	def set_degree_pursuing(self, val):
		'''
			Checks if the input value is valid before setting it.
		'''
		# Checks if the user is passing in the string value for degree pursuing.
		# If not, check if the int they're passing in is included in our dict.
		if (not(val in vals_degree_pursuing.values())):
			self.check_valid(val, vals_degree_pursuing, 
						s = " degree pursuing")
			self._degree_pursuing = vals_degree_pursuing[val]
		# If they are passing in a string, set the degree pursuing
		else:
			self._degree_pursuing = val

	degree_pursuing = property(get_degree_pursuing, set_degree_pursuing,
					doc = "Get and set degree pursuing.")

	def get_coding_ability(self):
		return self._coding_ability

	def set_coding_ability(self, val):
		'''
			Checks if the input value is valid before setting it.
		'''
		self.check_valid(val, vals_coding_ability, s = " coding ability")
		self._coding_ability = val

	coding_ability = property(get_coding_ability, set_coding_ability,
					 doc = "Get and set coding ability.")

	def get_business_ability(self):
		return self._business_ability

	def set_business_ability(self, val):
		'''
			Checks if the input value is valid before setting it.
		'''
		self.check_valid(val, vals_business_ability, s = " business ability")
		self._business_ability = val

	business_ability = property(get_business_ability, set_business_ability,
				doc = "Get and set business ability.")

	def get_work_experience(self):
		return self._work_experience

	def set_work_experience(self, val):
		'''
			Checks if the input value is valid before setting it.
		'''
		self.check_valid(val, vals_work_experience, s = " num yrs. work experience")
		self._work_experience = val

	work_experience = property(get_work_experience, set_work_experience,
					  doc = "Get and set the num. yrs. of work experience.")

	def get_project_rankings(self):
		return self._project_rankings

	def set_project_rankings(self, val, rankings_can_be_empty = False):
		'''
			Checks if the input value is valid before setting it.
		'''
                if duplicate_rankings:
                        alg_project_rnk = np.asarray(list(itertools.chain.from_iterable((e,e+num_valid_projects) for e in val)))
                else:
                        alg_project_rnk = val
		self.check_valid_project_rankings(alg_project_rnk, rankings_can_be_empty)
		self._project_rankings = alg_project_rnk

	project_rankings = property(get_project_rankings, set_project_rankings,
					  doc = "Get and set the project rankings.")

	def set_valid_properties(self, degree_pursuing, cod_abil, bus_abil, num_yrs_work_exp, 
							project_lst, rankings_can_be_empty = False):
		'''
			Checks if all input values are valid before setting them.
			Called from the Student constructor.
		'''
		self.set_degree_pursuing(degree_pursuing)
		self.set_coding_ability(cod_abil)
		self.set_business_ability(bus_abil)
		self.set_work_experience(num_yrs_work_exp)
		self.set_project_rankings(project_lst, rankings_can_be_empty)

	def check_valid(self, val, lst, s=""):
		'''
			If val is not included in lst, then we raise a FieldError.

			Parameters
			----------
			val: the value that is being passed into the Student constructor.
			lst: the list of valid values to check against.

			Returns
			-------
			If val is in lst, returns nothing. Otherwise, raises a FieldError.

		'''
		if (not (val in lst)):
		 	error = "Invalid input " + str(val) + " for student " + str(self._ID)
		 	error +=  " for field" + s + "."
		 	raise FieldError(error)
		else:
		 	pass

	def get_student_properties(self):
		'''
			Returns a list of the Student's properties.
		'''
		lst = []
		lst.append(self._name)
		lst.append(self._ID)
		lst.append(self._degree_pursuing)
		lst.append(self._business_ability)
		lst.append(self._coding_ability)
		lst.append(self._work_experience)
		lst.append(self._project_rankings)
                lst.append(self._bin_field)
		return lst

	def get_numerical_student_properties(self):
		'''
			Returns a list of the Student's properties.
			If degree_pursuing was stored as a string, this function will convert
			the string to an int ("MBA" = 0, "MEng" = 1).
		'''
		lst = []
		if (self._degree_pursuing == 0 or self._degree_pursuing == "MBA"):
			lst.append(0)
		elif (self._degree_pursuing == 1 or self._degree_pursuing == "MEng"):
			lst.append(1)
                elif (self._degree_pursuing == 2 or self._degree_pursuing == "HT"):
                        lst.append(2)
                elif (self._degree_pursuing == 3 or self._degree_pursuing == "CM"):
                        lst.append(3)
		else:
			raise ValueError("What kind of program is the student pursuing?")
		lst.append(self._business_ability)
		lst.append(self._coding_ability)
                lst.append(self._work_experience)
                lst.append(self._bin_field)
		return lst

	def get_ranking(self, project_id): 
		'''
			Get the number that this student ranked this project. 
			Returns 100 if the student did not rank the project.
		'''
		try:
			rankings = self._project_rankings.tolist()
			ind = rankings.index(project_id)
			return (ind + 1)
		except(ValueError):
			# Student did not rank this project.
			return 100

	def get_cost_from_ranking(self, rank):
		'''
			Get the cost of assigning a student to a given project rank.
			
			If the rank is within the number of project rankings,
			then we return the square of the rank. 

			This ensures that it is increasingly expensive to assign
			a student to a low rank. For example:
			rank 1 = cost of 1, rank 8 = cost of 64, rank 10 = cost of 100.

			If the rank is not within the number of project rankings,
			then we return 10^15. This places a serious penalty on assigning
			a student to a project that he/she did not rank.

			Parameters
			----------
			rank: int.

			Returns
			--------
			cost: int 
		'''
                if duplicate_rankings:
                        rank = (rank + 1)/2
		if (not(rank <= number_project_rankings)):
			return 1000000000000000
		else:
			return (rank * rank)

	def check_valid_project_rankings(self, val, rankings_can_be_empty = False):
		'''
	   		Iterates through the list of project rankings to check that they are
	  	 	1) unique
     		2) valid values (as specified by vals_valid_projects). 

			Parameters
			----------
			val: list of rankings, each represented by a project ID (int list).

			Returns
			-------
			Nothing, if val conforms to constraints 1) and 2) above.
			If not, this function will raise a FieldError.
	
		'''

		try:
			if (len(val) == 0 and rankings_can_be_empty):
				self._project_rankings = val
			elif (not (len(val) == alg_number_project_rankings)):
				error = "There must be " + str(number_project_rankings)
				error += " project rankings."
				raise FieldError(error)
		except TypeError:
			raise FieldError("Project rankings must be inputted as a list.")

		past = []
		for elm in val:
			self.check_valid(elm, vals_valid_projects, s = " project ID")
			if (elm in past):
				error = "Student " + str(self._ID) + " entered project "
				error += str(elm) + " twice."
				raise FieldError(error)
			past.append(elm)

class Project(object):
	def __init__(self, ID, capacity, capacity_w):
		'''
			Parameters
			----------
			ID: Project's ID (int)
                        capacity: The capacity per project (5 for 2015-2016) 
                        capacity_w: The capacity per project with wiggle-room (6 for 2015-2016)
		'''
		self.set_ID(ID)
		self.set_capacity(capacity)
		self.set_capacity_w(capacity_w)
		self._remaining_spots = capacity
                self._students = []
                # Waiting students is meant to be tuples of (rank, student) form.
		# I.e. (2, Ameya)  means that Ameya ranked this project 2 and is waiting.
		self._waiting_students = []

	def check_valid_student_nums(self, num_students):
		'''
			Checks that num_students is an integer greater than 0.
			To be used in checking that the values for num_MBAs and num_MEngs
			are valid.
		'''
		try:
			if(num_students < 0):
				error = "Number of required MBAs and MEngs must be positive."
				raise FieldError(error)
		except(TypeError):
			error = "Number of required MBAs and MEngs must be integers."
			raise FieldError(error)

	# Creating properties for all attributes of a Project object.
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


        def force_ID(self, val):
                '''
                    Force the project ID to be val.
                '''
                self._ID = val

	ID = property(get_ID, set_ID,
				  doc = "Get and set the team's ID, if not in the existing IDs.")
        
        def get_capacity(self):
                return self._capacity
        
        def set_capacity(self, val):
                self.check_valid_student_nums(val)
                self._capacity = val

        capacity = property(get_capacity, set_capacity,
                                                doc = "Get and set the capacity of this project.")


        def get_capacity_w(self):
                return self._capacity_w

        def set_capacity_w(self, val):
                self.check_valid_student_nums(val)
                if (val >= self._capacity):
                        self._capacity_w = val
                else:
                        raise FieldError("Wiggle capacity cannot be lower than the regular capacity")

        capacity_w = property(get_capacity_w, set_capacity_w,
                              doc = "Get and set the wiggle capacity of this project.")

	def get_students(self):
		return self._students

	def set_students(self, students):
		self._students = students

	students = property(get_students, set_students, 
						doc = "Get and set the students on this project.")

	def get_waiting_students(self):
		return self._waiting_students

	def set_waiting_students(self, val):
		error = "Cannot manually set the waiting students list."
		error += "Must add students via add_waiting_student function."
		raise FieldError(error)

	waiting_students = property(get_waiting_students, set_waiting_students, 
					   doc = "Get and set the waiting students for this project. ")

	def get_remaining_spots(self):
		return self._remaining_spots

	def set_remaining_spots(self, val):
		error = "Cannot manually set the remaining MBA spots."
		raise FieldError(error)

	remaining_spots = property(get_remaining_spots, set_remaining_spots,
				  doc = "Get and set the remaining spots on this project.")

	def has_remaining_spots(self):
		'''
			Returns a bool indicating if the project has any spots remaining.
			The spot could be for an MEng or an MBA.
		'''
                return (self._remaining_spots > 0)
 
	def has_waiting_students(self):
		'''
			Returns a bool indicating if the project has any students waiting
			to join the project.
		'''
		return (len(self.waiting_students) > 0)

	def add_student(self, student, wiggle, verbose = False):
		'''
			Parameters
			----------
			student: Student to add to the project (Student).
			wiggle: indicates if we would like "wiggle room" or not (bool).
			    If wiggle is True, then we will add one extra Student to
			    the project (i.e. will make a project of 4 into one of 5).
			    Note: will only add *one* extra Student.
			    If wiggle is False, then we will only have the specified
			    number of Students on the Project.
			verbose: indicates if we want to print updates (bool).

			Returns
			-------
			bool indicating if the add was successful.

			If possible, adds student to the current Project (self), and returns True. 
			Otherwise, does not modify the Project, and returns False.

		'''
		if (student.degree_pursuing == "MBA" or student.degree_pursuing == 0):
			if (verbose):
				print "Adding an MBA. ID is " + str(student.ID)
                elif (student.degree_pursuing == "MEng" or student.degree_pursuing == 1):
			if (verbose):
				print "Adding an MEng. ID is " + str(student.ID)
                elif (student.degree_pursuing == "HT" or student.degree_pursuing == 2):
                        if (verbose):
                                print "Adding a Health Tech. ID is " + str(student.ID)
                elif (student.degree_pursuing == "CM" or student.degree_pursuing == 3):
                        if verbose:
                                print "Adding a Connective Media. ID is " + str(student.ID)
                else:
                        raise FieldError("Is there a fifth program we are unaware of?")
                if (not(self.has_remaining_spots())):
                        if (wiggle):
                                if (len(self._students) < self._capacity_w):
                                        self._students.append(student)
                                        return True
                                else:
                                        if (verbose):
                                                print "This project does not have enough spots."
                                        return False
                else:
                        if (student in self._students):
                                return False
                        self._students.append(student)
                        self._remaining_spots -= 1
                        return True

	def add_waiting_student(self, student, verbose = False):
		'''
			Parameters
			----------
			student: Student to add to the waiting list of this Project.
			verbose: indicates if we want to print updates (bool). 

			Returns
			-------
			Nothing. Adds student to the waiting list.

		'''
		if (student in self._students):
			pass
		else:
			# Get the rank that this student gave this project.
			rank = student.get_ranking(self._ID)
			# Create a tuple of the project ranking and the student.
			tup = (rank, student)
			# Add the tuple to the waiting students list.
			self._waiting_students.append(tup)

                        
        def remove_student(self, student):
                self._students.remove(student)
                self._remaining_spots += 1


        def reset(self):
                self._students = []
                self._waiting_students = []
                self._remaining_spots = self._capacity

        def inv_get_ranking(self, student):
                return student.get_ranking(self._ID)

	def is_empty(self):
		'''
			Returns a bool indicating if the Project is empty.
			An empty project is one that has no Students.
		'''
		return (self._remaining_spots == self._capacity)

	def calculate_diversity(self, tup):
		'''

			Calculates the diversity as Mahalanobis distance of the numerical
			attributes of the Students' properties.

			Parameters
			----------
			tup: a tuple of the form (inv_cov_mat, dict_key_vals).
				 inv_cov_mat is the inverse of the covariance matrix of
				 the numerical attributes of the Students.
				 This is used for the Mahalanobis distance of all pairs
				 of students in the team.
				 dict_key_vals: a dictionary of student IDs and attributes.

			Returns
			-------
			diversity: the calculated diversity (float).

		'''
		inv_cov_mat = tup[0]
		dict_key_vals = tup[1]
		diversity = 0
		num_students = len(self._students)
		if (num_students < self._capacity):
			error = "Students on project " + str(self.ID) + " are "
			error += str([s.ID for s in self.students]) + ". This project is not full."
			error += " Cannot calculate diversity."
			raise ValueError(error)
		else:
			attributes = []
                        for student in self._students:
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
				d = distance.do_python_distance_data(fst_properties,
					snd_properties, inv_cov_mat)
				diversity += d
	 	return diversity



