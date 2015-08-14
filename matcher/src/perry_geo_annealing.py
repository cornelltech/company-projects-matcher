import numpy as np
import util
from classes import CompError
from numpy import random
import pdb

def energy(state):
	'''
		Calculates the energy of a given state.
	'''
	projects = state[0]
	inv_cov_mat_tup = state[1]

	def team_cost():
		diversities = []
                project_costs = []
                penalties = 0
		for project in projects:
                        costs = []
			project_diversity = project.calculate_diversity(inv_cov_mat_tup)
			diversities.append(project_diversity)
                        numerics = []
                        for student in project.students:
                                rank = student.get_ranking(project.ID)
                                cost = student.get_cost_from_ranking(rank)
                                costs.append(cost)
                                numerics.append(student.get_numerical_student_properties())
                        avg_project_cost = np.mean(costs)
                        project_costs.append(avg_project_cost)
                        programs = [x[0] for x in numerics]
                        b_abilities = [x[1] for x in numerics]
                        c_abilities = [x[2] for x in numerics]
                        w_exp = [x[3] for x in numerics]
                        #penalty for no MBAs
                        if 0 not in programs:
                                penalties += 1000
                        #penalty for no MEngs
                        if 1 not in programs:
                                penalties += 1000
                        #penalty for lack of coding experience (i.e. no one who rated their own coding ability as 3 or more)
                        if 3 not in c_abilities and 4 not in c_abilities:
                                penalties += 1000
                        #penalty for a lack of business ability
                        if 3 not in b_abilities and 4 not in b_abilities:
                                penalties += 1000
                        #penalty for lack of work experience
                        if 3 not in w_exp and 4 not in w_exp:
                                penalties += 1000
		avg_diversity = np.mean(diversities)
                ranking_cost = np.mean(project_costs)
		return 2*(ranking_cost) - (0.5 * avg_diversity) + penalties

	return team_cost()

def move(state, verbose = False, super_verbose = False):
	'''
		Makes a random change to a state.
		
		Picks two random teams, picks two random members, and performs
		a swap of these members across the teams.

                With some small probability, change a project to a completely different project instead.
		NOTE: there should be no teams of size 0 before calling the function.	
	'''
        project_exchange_probability = 0.01

	projects = state[0]
	inv_cov_mat_tup = state[1]
        feasibles = state[2]

        if random.random() < project_exchange_probability:
                project_to_swap = util.random_project(projects, [], True)
                feasible_IDs = [p.ID for p in feasibles]
                reasonable_project_IDs = list(set().union(*[set(s.project_rankings) for s in project_to_swap.students]))
                reasonable_projects = filter(lambda p:p.ID in reasonable_project_IDs, feasibles)
                def popularity(p):
                        return len(filter(lambda s:s.get_ranking(p.ID) < 100,project_to_swap.students))
                reasonable_projects.sort(key=popularity, reverse = True)
                most_likely_popular = reasonable_projects[:max(10, 2*len(projects))]
                other = util.random_project(most_likely_popular, projects, False)
                if other == None:
                        pass
                else :
                        tmp = project_to_swap.ID
                        projects.remove(project_to_swap)
                        projects.append(other)
                        util.safe_project_swap(project_to_swap, other)
        else: 
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
                # while (not (student_one.degree_pursuing == student_two.degree_pursuing)):
                #	student_two = util.random_student(second_team)

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

	state_after_change = (projects, inv_cov_mat_tup, feasibles)

	#print energy(state_after_change)

	return projects

def energy_co(state):
        projects = state[0]
	inv_cov_mat_tup = state[1]

	def team_cost():
		diversities = []
                project_costs = []
                penalties = 0
		for project in projects:
                        costs = []
			project_diversity = project.calculate_diversity(inv_cov_mat_tup)
			diversities.append(project_diversity)
                        for student in project.students:
                                rank = student.get_ranking(project.ID)
                                cost = student.get_cost_from_ranking(rank)
                                costs.append(cost)
                        avg_project_cost = np.mean(costs)
                        project_costs.append(avg_project_cost)
                avg_diversity = np.mean(diversities)
                ranking_cost = np.mean(project_costs)
		return 2*(ranking_cost) - (0.5 * avg_diversity) + penalties

	return team_cost()


def move_co(state, verbose = False, super_verbose = False):
        '''
                A move for conversations in the studio. There are exactly classes.number_project_rankings
                groups, so it does not make any sense to allow projects to change identity. In its place,
                this move type will swap a student that is matched with a student that is unmatched.
        '''

        student_exchange_probability = 0.01

	projects = state[0]
	inv_cov_mat_tup = state[1]
        feasibles = state[2]
        students = state[3]

        if random.random() < student_exchange_probability:
                project_to_choose_from = util.random_project(projects, [], True)
                student_to_swap = util.random_student(project_to_choose_from)
                matched_students = []
                for p in projects:
                        matched_students.extend(p.students)
                other = util.random_student_lst(students, matched_students, False)
                if other == None:
                        pass
                else :
                        project_to_choose_from.students.remove(student_to_swap)
                        project_to_choose_from.students.append(other)
        else: 
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
                # while (not (student_one.degree_pursuing == student_two.degree_pursuing)):
                #	student_two = util.random_student(second_team)

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

	state_after_change = (projects, inv_cov_mat_tup, feasibles)

	#print energy(state_after_change)

	return projects
