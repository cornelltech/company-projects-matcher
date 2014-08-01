import numpy as np

# A function to calculate the energy of a state.
# #38: did not include diversity yet. Will add that after.
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








