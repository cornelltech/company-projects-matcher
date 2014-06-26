import abc

#TODO: should these say valuable things?

vals_cs_ug = [True, False]
vals_work_experience = range(0, 7)

dict_coding_ability = { 0 : "none",
						1 : "a little exposure",
						2 : "medium",
						3 : "good",
						4 : "excellent"
}

dict_technical_strength = { 1 : "frontend",
							  	2 : "backend",
							  	3 : "UX",
							   	4 : "mobile",
							   	5 : "systems/hardware",
							   	6 : "databases",
								7 : "algorithms",
								8 : "graphics",
}

class StudentFieldError(Exception):
	def __init__(self, value):
		self.val = value
	def __str__(self):
		return repr(self.val)

class Student(object):

	#__metaclass__ = abc.ABCMeta

	global vals_cs_ug
	global vals_yrs_work_experience
	global dict_coding_ability
	global dict_technical_strength

	#@abc.abstractmethod
	def __init__ (self, name, ID, ca=None, csug=None, tts=None, nywe=None):
		''' 
			Parameters
			----------
			ca    = coding ability. Int from 0 to 4, inclusive.
			csug  = was cs undergrad. Boolean.
			tts   = type of technical strength. TechnicalStrength class/enum.
			nywe  = num. years of work experience. Int from 0 to 6 (6 = 6+).

		'''
		
		self._name				 	  = name
		self._ID				 	  = ID
		self._coding_ability 		  = ca
		self._was_cs_ug 		 	  = csug
		self._type_technical_strength = tts
		self._work_experience 	 	  = nywe
		
	# TODO: add a global dict that will map ints to types of technical strength.
	# TODO: in "set_technical_strength", convert that int to a string.	


	def check_valid_coding_ability(self, val):
		# if (not (val in dict_coding_ability)):
		# 	error = "Invalid input " + str(val) + " for student " + self._ID + "'s coding ability."
		# 	raise StudentFieldError(error)
		# else:
		# 	pass
		pass

	def set_valid_properties(ca, csug, tts, nywe):

		pass

	# Defining properties
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

	def get_coding_ability(self):
		return self._coding_ability

	def set_coding_ability(self, val):
		self.check_valid_coding_ability(val)
		self._coding_ability = val

	coding_ability = property(get_coding_ability, set_coding_ability,
					 doc = "Get and set coding ability.")

	def get_cs_ug(self):
		return self._was_cs_ug

	# TODO: make sure that this is actually valid with 0 and 1 for val.
	def set_cs_ug(self, val):
		if (not (val in vals_cs_ug)):
			error = "Invalid input " + str(val) + " for student " + self._ID + "'s was CS undergrad field."
			raise StudentFieldError(error)
		else:
			self._was_cs_ug = val

	was_cs_ug = property(get_cs_ug, set_cs_ug,
				doc = "Get and set if student was a CS undergrad.")

	def get_technical_strength(self):
		return dict_technical_strength[self._type_technical_strength]

	def set_technical_strength(self, val):
		if (not (val in dict_technical_strength)):
			error = "Invalid input " + str(val) + " for student " + self._ID + "'s type of technical strength."
			raise StudentFieldError(error)
		else:
			self._type_technical_strength = dict_technical_strength[val]

	type_technical_strength = property(get_technical_strength, set_technical_strength,
						doc = "Get and set the type of the student's technical strength.")

	def get_work_experience(self):
		return self._work_experience

	def set_work_experience(self, val):
		if (not (val in vals_work_experience)):
			error = "Invalid input " + str(val) + " for student " + self._ID + "'s work experience."
			raise StudentFieldError(error)
		else:
			self._work_experience = val

	work_experience = property(get_work_experience, set_work_experience,
					  doc = "Get and set the num. yrs. of work experience.")



	