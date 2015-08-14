#!/usr/bin/env python

import util
import initial_solution
import numpy as np
import copy
import random
import classes
import distance
import clustering
from scipy import stats

def random_student(student_ID):
    xs1 = np.arange(4)
    ps1 = (.32,.36,.05,.26)
    program_random = stats.rv_discrete(name='progs', values=(xs,ps))


    program = random.randint(0,3)
    business_ability = random.randint(0,4)
    coding_ability = random.randint(0,4)
    work_experience = random.randint(0,4)
    return classes.Student("noname noname", student_ID, program, business_ability,coding_ability,work_experience,[], rankings_can_be_empty = True)

if (__name__ == "__main__"):
    #generate 1000 students
    '''students = [random_student(i) for i in range(1000)]
    inv_cov_mat_tup = distance.create_inv_cov_mat_from_data(False, students, None)
    print inv_cov_mat_tup
    print(len(students))
    print(inv_cov_mat_tup[0].shape)
    for s in students:
        print s.get_numerical_student_properties()'''
    
    students = util.create_students_from_input('students.csv')
    inv_cov_mat_tup = distance.create_inv_cov_mat_from_data(False, students,None)
    projects = [classes.Project(i, 5, 6) for i in range(1,2001)]
    diversities = []
    for p in projects:
        p.students = np.random.choice(students, 5, replace=False).tolist()
        diversities.append((p.ID,p.calculate_diversity(inv_cov_mat_tup)))
        
    def keyval(tup):
        return tup[1]

    diversities.sort(key = keyval, reverse = True)

    print "The hundred most diverse teams are: " + str([vals for vals in diversities[:100]])
    for team in [vals[0] for vals in diversities[:100]]:
        print "Team " + str(projects[team-1].ID) + " has numerical properties:"
        for s in projects[team-1].students:
            print s.get_numerical_student_properties()

    print "The hundred least diverse teams are: " + str([vals for vals in diversities[-100:]])
    for team in [vals[0] for vals in diversities[-100:]]:
        print "Team " + str(projects[team-1].ID) + " has numerical properties:"
        for s in projects[team-1].students:
            print s.get_numerical_student_properties()
