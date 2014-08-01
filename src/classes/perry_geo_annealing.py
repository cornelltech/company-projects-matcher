import numpy as np
import random_teams

# A function to calculate the energy of a state.
def energy(state):
	projects = state[0]
	unmatched_students = state[1]
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

	def unmatched_student_cost():
		return 10000 * len(unmatched_students) 

	# 34
	def team_diversity_cost():
		return 0

	return avg_project_costs() + unmatched_student_cost() + team_diversity_cost()

# A function to make a random change to a state.
# Returns None (just like the example).
# Currently implemented as one swap of two people across teams.
def move(state):
	projects = state[0]
	#unmatched_students = state[1]

	project_one = random_teams.random_project(projects)
	project_two = random_teams.random_project(projects)

	# Team to pick first students from 
	pick_team = random_teams.random_two_choice()

	if (pick_team == 0):
		first_team = project_one
		second_team = project_two
	else:
		first_team = project_two
		second_team = project_one

	# Pick a student from the first team, and this student will be swapped.
	student_one = random_teams.random_student(first_team)
	student_two = random_teams.random_student(second_team)

	# NOTE: this is problematic if teams aren't full.
	# 38
	while (not (student_one.degree_pursuing == student_two.degree_pursuing)):
		student_two = random_teams.random_student(second_team)

	# Remove the students from their respective teams
	first_team.students.remove(student_one)
	second_team.students.remove(student_two)

	first_team.add_student(student_two)
	second_team.add_student(student_one)










