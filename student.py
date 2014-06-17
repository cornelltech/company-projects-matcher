import abc

class Student(object):

	#__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def __init__ (self, ca, csug, tts, nywe):
		''' Arguments passed in as:
			ca    = coding ability. Int from 0 to 4, inclusive.
			csug  = was cs undergrad. Boolean.
			tts   = type of technical strength. TechnicalStrength class/enum.
			nywe  = num. years of work experience. Int from 0 to 6 (6 = 6+).'''
		
		self._coding_ability 	 = ca
		self._was_cs_ug 		 = csug
		self._technical_strength = tts
		self._work_experience 	 = nywe

	# Defining proerties
	def get_coding_ability(self):
		return self._coding_ability

	def set_coding_ability(self, val):
		self._coding_ability = val

	coding_ability = property(get_coding_ability, set_coding_ability, doc = "Get and set coding ability.")

	def get_cs_ug(self):
		return self._was_cs_ug

	def set_cs_ug(self, val):
		self._was_cs_ug = val

	was_cs_ug = property(get_cs_ug, set_cs_ug, doc = "Get and set if student was a CS undergrad.")

	def get_technical_strength(self):
		return self._technical_strength

	def set_technical_strength(self, val):
		self._technical_strength = val

	technical_strength = property(get_technical_strength, set_technical_strength, doc = "Get and set technical strength.")

	def get_work_experience(self):
		return self._work_experience

	def set_work_experience(self, val):
		self._work_experience = val

	work_experience = property(get_work_experience, set_work_experience, doc = "Get and set work experience.")



	