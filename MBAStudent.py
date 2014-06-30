from student import Student

# class MBAStudent(Student):

# 	def __init__(self, name, ID, ca, csug, tts, nywe):
# 		# Initially just calling superclass init, 
# 		# but has room for adding new attributes
# 		# specific to an MBA student. 
# 		super(MBAStudent, self).__init__(name, ID, ca, csug, tts, nywe)

# Random test cases for proper use of inheritance / getters and setters. 
if __name__ == "__main__":

 # 	def __init__ (self, name, ID, degree_pursuing, cod_abil, cs_ug, type_tech_stren, num_yrs_work_exp):

	a = Student("Ameyayayaya", 2886650, "MBA", 3, False, "databases", 9)
	print a.name
	print a.ID
	print a.coding_ability
	print a.was_cs_ug
	print a.type_technical_strength
	print a.work_experience

	# print "a's technical strength is"
	# print a.type_technical_strength
# 	print "setting a's technical strength to 5"
# 	a.technical_strength = 5
# 	print "a's new technical strength is"
# 	print a.technical_strength