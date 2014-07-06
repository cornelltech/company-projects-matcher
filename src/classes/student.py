import random

'''To ensure that we do not create multiple teams with the same ID.'''
existing_team_IDs = []
existing_student_IDs = []

# Declaring valid values for all fields.
vals_cs_ug = [True, False]
vals_work_experience = range(0, 7)

# 0 = lowest, 4 = most
vals_coding_ability = range(0, 5)

# Keep these organized in alphabetical order. 
vals_degree_pursuing = { 0 : "MBA",
						 1 : "MEng"
}

# Valid IDs for our projects.
vals_valid_projects = map(lambda x: x * 65, range(16, 66))

degree_weight = 0.25
cs_ug_weight = 0.25
coding_ability_weight = 0.25
work_experience_weight = 0.25

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

	def set_project_rankings(self, val):
		# Because val is a list and we want to check if each of the projects 
		# has a valid ID
		try:
			if (not (len(val) == 10)):
				raise FieldError("There must be 10 project rankings.")
		except TypeError:
			raise FieldError("Project rankings must be inputted as a list.")

		past = []
		for elm in val:
			self.check_valid(elm, vals_valid_projects, s = " project ID")
			if (elm in past):
				raise FieldError("Each project can only be entered once.")
			past.append(elm)
	
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
			nywe  = num. years of work experience. Int from 0 to 6 (6 = 6+).
			project_lst = an integer list size 10. Ints are the project IDs. 
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

	def get_ranking(self, project_id):
		try:
			rankings = (self._project_rankings).tolist()
			ind = rankings.index(project_id)
			return ind
		except(ValueError):
			error_one = "Project " + str(project_id) + " is not in student "
			error_two = "'s ranking list."
			raise FieldError(error_one + self._ID.astype('|S10') + error_two)

	def get_interest_from_ranking(self, rank):
		return abs(10 - rank)

class Team(object):

	global degree_weight
	global cs_ug_weight
	global coding_ability_weight
	global work_experience_weight

	def __init__(self, student_list, ID=-1):
		for student in student_list:
			if (student.ID in existing_student_IDs):
				error = "Student ID " + str(student.ID) + " is already taken."
				raise FieldError(error)
		if ((len(student_list) == 4) or (len(student_list) == 5)):
			self._members = student_list
		else:
			raise FieldError("Team size must be 4 or 5.")
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

		diff_degrees = self.calculate_pairwise_differences(degrees, False)
		diff_csugs = self.calculate_pairwise_differences(csugs, False)
		diff_coding_abilities = self.calculate_pairwise_differences(coding_abilities)
		diff_work_experiences = self.calculate_pairwise_differences(work_experiences)
		
		print "Deg:",
		print diff_degrees
		print "Csug:",
		print diff_csugs
		print "Coding abilities:",
		print diff_coding_abilities
		print "Work experience:",
		print diff_work_experiences

		return [diff_degrees, diff_csugs, diff_coding_abilities, diff_work_experiences]

	def do_diversity_calculation(self):
		pairwise_differences = self.calculate_all_pairwise_differences()
		
		normal_avg = self.avg_list(pairwise_differences)

		degree_weight = 0.5
		csug_weight = 0.1
		coding_weight = 0.3
		work_weight = 0.1

		deg = pairwise_differences[0]
		cs = pairwise_differences[1]
		cod = pairwise_differences[2]
		work = pairwise_differences[3]

		weighted_avg = degree_weight*deg + coding_weight*cod + csug_weight*cs + work_weight*work

		print "Normal sum is",
		print normal_avg
		print "Weighted sum is",
		print weighted_avg


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













