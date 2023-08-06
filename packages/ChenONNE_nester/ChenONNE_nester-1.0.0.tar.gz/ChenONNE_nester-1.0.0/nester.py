"""This is "nester.py" module, which provides a function named print_lol() that print a list, while the list may (or not) contain a nested list."""
 
def print_lol(the_list):
	"""This function get a parameter called "the_list", which can be any Python List(also can be a list contain list). All data in the list will be printed on the screen in a line"""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item)
		else:
			print(each_item)


