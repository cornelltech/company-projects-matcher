from student import Student

class MBAStudent(Student):

	def __init__(self, name, ID, ca, csug, tts, nywe):
		# Initially just calling superclass init, 
		# but has room for adding new attributes
		# specific to an MBA student. 
		super(MBAStudent, self).__init__(name, ID, ca, csug, tts, nywe)

# Random test cases for proper use of inheritance / getters and setters. 
if __name__ == "__main__":

	a = MBAStudent("Name", 2886650, 1, 2, "Algorithms", 4)
	print "a's technical strength is"
	print a.type_technical_strength
# 	print "setting a's technical strength to 5"
# 	a.technical_strength = 5
# 	print "a's new technical strength is"
# 	print a.technical_strength