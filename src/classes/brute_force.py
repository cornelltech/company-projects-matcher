import exhaustive

def function_one(projects, students):
	pass

def do_tests():
	students_lst = exhaustive.get_students_from_input("tests.csv")
	filtered_projects = exhaustive.remove_infeasible_projects(students_lst)
	function_one(filtered_projects, students_lst)
	pass