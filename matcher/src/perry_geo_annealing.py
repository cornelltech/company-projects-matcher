import numpy as np
import util
from classes import CompError

# A function to calculate the energy of a state.
def energy(state):
	projects = state[0]
	inv_cov_mat_tup = state[1]

	# Averages the costs on each project, and then averages across all projects.
	def avg_project_costs():
		project_costs = []
		for project in projects:
			costs = []
			for student in project.students:
				rank = student.get_ranking(project.ID)
				cost = student.get_cost_from_ranking(rank)
				costs.append(cost)
			avg_project_cost = np.mean(costs)
			project_costs.append(avg_project_cost)
		energy = np.mean(project_costs)
		return energy

	# 34
	def team_diversity_cost():
		diversities = []
		for project in projects:
			project_diversity = project.calculate_diversity(inv_cov_mat_tup)
			diversities.append(project_diversity)
		avg_diversity = np.mean(diversities)
		return 1 / avg_diversity

	return avg_project_costs() + team_diversity_cost()

# A function to make a random change to a state.
# Returns None (just like the example).
# Currently implemented as one swap of two people across teams.
# NOTE: there should be no teams of size 0 before calling the function.
def move(state, verbose = True, super_verbose = False):
	projects = state[0]
	inv_cov_mat_tup = state[1]

	project_one = util.random_project(projects, [], True)
	project_two = util.random_project(projects, [], True)


	# Guarantee that the projects are not the same.
	# Continue to swap project two until it is diff from project one.
	while (project_one.ID == project_two.ID):
		project_two = util.random_project(projects, [], True)
		if (super_verbose):
			print "Project one and project two are the same."

	if (super_verbose):
		print "Found two different projects."

		print "First team students are " + str([s.ID for s in project_one.students])
		print "Second team students are " + str([s.ID for s in project_two.students])

		print "CLEAR: made it to pick_team"

	# Team to pick first students from 
	pick_team = util.random_two_choice()

	if (pick_team == 0):
		first_team = project_one
		second_team = project_two
	else:
		first_team = project_two
		second_team = project_one

	# Pick a student from the first team, and this student will be swapped.

	student_one = util.random_student(first_team)
	student_two = util.random_student(second_team)

	# NOTE: this is problematic if teams aren't full.
	# 38
	# Guarantee that the students are of the same type.
	while (not (student_one.degree_pursuing == student_two.degree_pursuing)):
		student_two = util.random_student(second_team)

	# Remove the students from their respective teams
	first_team.students.remove(student_one)
	if (not(student_two in second_team.students)):
		if (super_verbose):
			print "Second team students is " + str([s.ID for s in second_team.students])
		error = "Student two ("
		error += str(student_two.ID)
		error += ") is not in second_team.students ("
		error += str(second_team.ID)
		error += ") "
		
		raise CompError(error)
	second_team.students.remove(student_two)

	first_team.students.append(student_two)
	second_team.students.append(student_one)

	if (verbose):
		print "AFTER MOVE:"
		for p in projects:
		 	print str(p.ID) + ": " + str([s.ID for s in p.students])

	state_after_change = (projects, inv_cov_mat_tup)

	print energy(state_after_change)

	return projects

