import exhaustive
import itertools

def function_one(projects, students):
	for p in projects:
		#print "For " + names_projects[p.ID] + " project:"
		matched = filter(lambda x: p.ID in x.project_rankings, students)
		iterable = itertools.combinations(matched, 4)

		#Create list out of above iterable. List elements are tuples
		groups_of_four = []
		for g in iterable:
			groups_of_four.append(g)

		#print [(a.ID, b.ID, c.ID, d.ID) for (a, b, c, d) in groups_of_four]
		
		#Remove infeasible teams (i.e. less than 2 MEngs or 2 MBAs)
		impossible_teams = []
		for g in groups_of_four:
			MBAs_ranked = [s for s in g if s.degree_pursuing == 0]
			MEngs_ranked = [s for s in g if s.degree_pursuing == 1]
			if (len(MBAs_ranked) < 2 or len(MEngs_ranked) < 2):
				impossible_teams.append(g)

		feasible_teams = filter(lambda t: t not in impossible_teams, groups_of_four)
		#print str(p.ID) + ":" + str([(a.ID, b.ID, c.ID, d.ID) for (a, b, c, d) in feasible_teams])

		#print str(p.ID) + ":" + str(len(matched)) + " ranked, " + str(len(feasible_teams)) + " feasible teams."
		#print [(a.ID, b.ID, c.ID, d.ID) for (a, b, c, d) in feasible_teams]

		# 	projects.sort(key = lambda p: get_project_interest_from_rankings(p, students), reverse = True)

		# NOTE: this is per project.
		team_interest_tuples = []

		for t in feasible_teams:
			project_ranking = exhaustive.get_project_interest_from_rankings(p, students)
			# Create a tuple of this team's interest for the project and the team (a 4-tuple of students).
			tup = (project_ranking, t)
			team_interest_tuples.append(tup)





def do_tests():
	students_lst = exhaustive.get_students_from_input("tests.csv")
	filtered_projects = exhaustive.remove_infeasible_projects(students_lst)
	function_one(filtered_projects, students_lst)
	#print "hi"

if (__name__ == "__main__"):
	do_tests()
	