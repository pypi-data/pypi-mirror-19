import sys
'''This is the "nester.py" module. It provides one function called print_lol() which prints lists that may or may not include nested lists.'''
movies = ["The Holy Grail",1975,"Terry Jones & Terry Gilliam",91,
			["Graham Chapman",
				["Michael Palin","John Cleese","Terry Gilliam","Eric Idle","Terry Jones"]]]

def print_lol(the_list,indent=False,level=0,destination=sys.stdout):
	'''This function takes one positional argument called "the list" which is any Python list or nested list. Each data item in the provided list is
	recursively printed to the screen. The function also takes in a level argument to indent the output when a list is found. Another argument indent
	controls if indentation should be performed or not. Use true to indent. Added destination for location to write to.'''
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,indent,level+1,destination)
		else:
			if indent:
				for num in range(level):
					print("\t",end='',file=destination)
			print(each_item,file=destination)

#print_lol(movies,True,0)