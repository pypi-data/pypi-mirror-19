def print_log(arry_list):
	for each_item in arry_list:
		if isinstance(each_item,list):
			print_log(each_item)
		else:
			print(each_item)
