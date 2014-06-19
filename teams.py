def create_teams(types_and_sizes, team_sizes):
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

		types_and_sizes: a list of tuples of the form (student_type, num_students).
						By inputting a specific type of student, you are stating
						that you want at least one of that type of student on each
						team.

						For example: [(MBA, 39), (MEng, 35)].
						NOTE: for now the student "type" is really just a string.
						Will probably change that later.


		team_sizes: a list of possible sizes of teams. 
						For example: [3, 4]

		Returns
		--------

		teams: a list of tuples that represent teams. Each tuple will contain integers,
				which represent the IDs of the students in the team.
	'''
	print "hi"