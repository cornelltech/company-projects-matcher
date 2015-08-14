#!/usr/bin/env python

import util
import initial_solution
import numpy as np
import copy

if (__name__ == "__main__"):
    students = util.create_students_from_input('students.csv')
    print len(students)
    feasibles = util.create_feasible_projects(students, util.generate_all_projects())
    min_rank = float("inf")
    min_sol = None
    def calculate_avg_rank(solution, verbose = False):
        avgs = []
        cnt = 0
        for p in solution:
            cnt += len(p.students)
            if (verbose):
                print str(p.ID) + ":" + str([s.ID for s in p.students])
                print "Ranks:",
            rankings = [s.get_ranking(p.ID) for s in p.students]
            if (verbose):
                print rankings
            avg_rank = np.mean(rankings)
            if (verbose):
                print "Average rank: " + str(avg_rank)
            avgs.append(avg_rank)
        if (len(avgs)==0):
            raise ValueError('Tried to average slice of length 0.')
        overall_average_rank = np.mean(avgs)
        print "Number of students: " + str(cnt)
        return overall_average_rank
                        
    for offset in range(len(feasibles)):
        for project in feasibles:
            project.reset()
        cur_sol = initial_solution.greedy_initial_solution_and_fill_unmatched(students, feasibles, True)
        #inits = initial_solution.greedy_initial_solution_team_first(students, feasibles, offset)
        # cur_sol = initial_solution.randomly_add_unmatched_students(inits)
        cur_avg_rank = calculate_avg_rank(cur_sol)
        print "Solution " + str(offset) + " average rank: " + str(cur_avg_rank)
        if (cur_avg_rank < min_rank):
            min_rank = cur_avg_rank
            min_sol = copy.deepcopy(cur_sol)
    print "The minimum avg rank is " + str(min_rank)
    min_sol_projects = [p for p in min_sol if len(p.students) > 0]
    #print(calculate_avg_rank(min_sol_projects, True))
    print "The returned solution has an avg rank of " + str(calculate_avg_rank(min_sol_projects, verbose = False))
	

