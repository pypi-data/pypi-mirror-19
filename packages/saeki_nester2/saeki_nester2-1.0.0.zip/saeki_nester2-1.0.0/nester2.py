def print_www(the_movie):
	for every_item in the_movie:
		if isinstance(every_item,list):
			print_www(every_item)
		else:
			print(every_item)

