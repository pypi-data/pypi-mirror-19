"""This is "nester.py" module, which provides a function named print_lol() that print a list, while the list may (or not) contain a nested list."""
 
def print_lol(the_list,indent=False,level=0,fn=sys.stdout):
	"""This function get four parameters called "the_list", "indent", "level", "fn". "the_list" can be any Python List(also can be a list contain list). "indent" is a flag that instruct whether the list printed with indention. "level" decide the indention level(if indent is True). All data in the list will be printed to where "fn" points."""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,indent,level+1,fn)
		else:
			if indent:
				for num in range(level):
					print("\t",end='',file=fn)
			print(each_item,file=fn)


