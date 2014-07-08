import numpy as np 
import pandas as pd 

import classes
import itertools
import teams
from classes import Student
from classes import Team
from classes import Project
from classes import CompError
from classes import FieldError

student_ids = []

def normalize_bet_zero_and_one(lst):
	lst_max = lst.max()
	lst_min = lst.min()
	den = lst_max - lst_min
	num = [elm - lst_min for elm in lst]
	# TODO: get rid of this stupid error.
	if (den == 0):
		raise CompError("In normalizing our quantitative variables, all values are the same.")
	final = [(elm * 1.0) / den for elm in num]
	return final

def generate_all_projects(num_MBAs = 2, num_MEngs = 2):
	projects_lst = []
	for ID in classes.vals_valid_projects:
		p = Project(ID, num_MBAs, num_MEngs)
		projects_lst.append(p)
	return projects_lst

def exhaustive(projects, students):

	# Filter out projects with insufficient rankings to get matched.
	insufficient_IDs = []
	for p in projects:
		matched = filter(lambda x: p.ID in x.project_rankings, students)
		print "For project " + str(p.ID) + ":"
		print [s.ID for s in matched]
		MBAs_ranked = [s for s in matched if s.degree_pursuing == 0]
		MEngs_ranked = [s for s in matched if s.degree_pursuing == 1]
		print [s.ID for s in MBAs_ranked]
		print [s.ID for s in MEngs_ranked]

	 	if (len(MBAs_ranked) < 2 or len(MEngs_ranked) < 2):
	 		print "NOT ENOUGH MBAS OR MENGS"
	 		insufficient_IDs.append(p.ID)

	projects = filter(lambda p: not(p.ID in insufficient_IDs), projects)
	print [p.ID for p in projects]

	def get_project_interest_from_rankings(p):
		overall_interest = 0

		matched = filter(lambda x: p.ID in x.project_rankings, students)
		print "For project " + str(p.ID) + ":"
		print [s.ID for s in matched]
		for s in matched:
 			rank = s.get_ranking(p.ID)
			interest = s.get_interest_from_ranking(rank)
		 	print "Interest is "
		 	overall_interest = overall_interest + interest
		return overall_interest


	# Sort projects in order of highest demand to lowest demand.
	projects.sort(key = lambda p: get_project_interest_from_rankings(p), reverse = True)
	print [p.ID for p in projects]

	for p in projects:
		matched = filter(lambda x: p.ID in x.project_rankings, students)
		MBAs_ranked = [s for s in matched if s.degree_pursuing == 0]
		MEngs_ranked = [s for s in matched if s.degree_pursuing == 1]
		# Generate all possible pairs of MBAs.		
		iter_MBA_pairs = itertools.combinations(MBAs_ranked, 2)
		print "MBA pair IDS"
		MBA_pairs = []
		for s in iter_MBA_pairs:
			MBA_pairs.append(s)
			(x, y) = s
			print x.ID,
			print y.ID
		# Generate all possible pairs of MEngs.
		iter_MEng_pairs = itertools.combinations(MEngs_ranked, 2)
		print "MEng pair IDS"
		MEng_pairs = []
		for s in iter_MEng_pairs:
			MEng_pairs.append(s)
			(x, y) = s
			print x.ID,
			print y.ID
		print "MEng pairs is is "
		print MEng_pairs
		print "MBA pairs is "
		print MBA_pairs

		print "Len MBA pairs",
		print len(MBA_pairs)
		print "Len MEng pairs",
		print len(MEng_pairs)

		# Generate combinations of the MBAs and the MEngs.
		all_possible_teams = []
		for x in MBA_pairs:
			for y in MEng_pairs:
				all_possible_teams.append((x, y))

		print len(all_possible_teams)

		all_possible_teams_with_values = []
		for t in all_possible_teams:
			overall_interest = 0
			((x, y), (a, b)) = t
			members = [x, y, a, b]
			print "(",
			print x.ID,
			print ",",
			print y.ID,
			print ",",
			print a.ID,
			print ",",
			print b.ID,
			print ")",
			for mem in members:
				rank = mem.get_ranking(p.ID)
				interest = mem.get_interest_from_ranking(rank)
				overall_interest = overall_interest + interest
			all_possible_teams_with_values.append((overall_interest, t))

		# for a in all_possible_teams_with_values:
		# 	print "(" + str(a[0]) + ","
		# 	print type(a[1])
		# 	print str(a[1].ID) + ")"
		print ""
		print ""

		print all_possible_teams_with_values
		all_possible_teams_with_values.sort(key = lambda tup: tup[0], reverse = True)
		print all_possible_teams_with_values

		if (len(all_possible_teams_with_values) > 0):
			happiest_team_combo = (all_possible_teams_with_values[0])[1]
		else:
			# Should never reach this point.
			raise FieldError("There are no viable teams for project " + str(p.ID) + ".")

		print "Happiest team combo is"
		print happiest_team_combo

		print type(happiest_team_combo)

		print "Before removing, len of students is",
		print len(students)
		for tup in happiest_team_combo:
			for stud in tup:
				for s in students:
					if (s.ID == stud.ID):
						students.remove(s)
						print "Removed"
		print "After removing, len of students is",
		print len(students)

		# for a in all_possible_teams_with_values:
		# 	print "(" + str(a[0]) + ","
		# 	print str(a[1].ID) + ")"

		print "Projects currently are:"
		print projects
		#print [(b, e) for b in MBA_pairs for e in MEng_pairs]
		pass




# 	def get_ranking(self, project_id):
# 	def get_interest_from_ranking(self, rank):






































def read_input(file, normalize=True):
	data = pd.read_csv(file)
	data_array = np.array(data)
	shape = data_array.shape
	num_rows = shape[0]

	# Normalize our numerical variables to lie between 0 and 1.
	all_coding_abilities = data_array[:,3]
	all_work_experience = data_array[:,4]

	# TODO: instead of normalizing, should just scale it out of 1.
	# Normalization is too dependent on the values it's passed in with.
	scaled_coding_abilities = normalize_bet_zero_and_one(all_coding_abilities)
	scaled_yrs_work_experience = normalize_bet_zero_and_one(all_work_experience)
	
	students_lst = []

	# Extract rows
	for i in range(0, num_rows):
		student = data_array[i,:]
		ID 	= student[0]
		if (ID in student_ids):
			raise CompError("Student IDs must be unique.")
		student_ids.append(ID)
		
		degree_pursuing = student[1]
		cs_ug = student[2]
		coding_ability = student[3]
		num_yrs_work_exp = student[4]

		# Only take the desired number of project rankings that we want.
		rankings = student[5:(5 + classes.number_project_rankings)]

		scaled_coding_ability = scaled_coding_abilities[i]
		scaled_num_yrs_work_exp = scaled_yrs_work_experience[i]

		a = Student("Test", ID, degree_pursuing, cs_ug, coding_ability, num_yrs_work_exp, rankings)

		if (normalize):
			a = Student("Test", ID, degree_pursuing, cs_ug, scaled_coding_ability, scaled_num_yrs_work_exp, rankings, True)

		students_lst.append(a)

	projects = generate_all_projects()

	for p in projects:
		p.print_student_IDs()

	exhaustive(projects, students_lst)

if (__name__ == "__main__"):
		read_input("tests.csv")