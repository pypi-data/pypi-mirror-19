def print_lol(the_list, indent=False, num=0):
	for each_item in the_list:
		if isinstance (each_item, list):
			print_lol(each_item, indent, num+1)
		else:
			if indent :
				print("\t"*num, end='')
			print(each_item)