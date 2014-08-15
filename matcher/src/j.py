import util

dictionary = util.read_project_ids_and_names_from_input()
for key in dictionary.keys():
	print dictionary[key]
