def print_lol(the_list, num):
	for each_item in the_list:
		if isinstance (each_item, list):
			print_lol(each_item, num+1)
		else:
			for count in range(num):
				print("\t", end='')
			print(each_item)