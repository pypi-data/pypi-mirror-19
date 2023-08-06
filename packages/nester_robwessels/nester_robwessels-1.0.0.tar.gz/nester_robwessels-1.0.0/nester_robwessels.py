
"""nester.py module, created by: RJM Wessels, 6 december 2016"""
def print_lol(the_list):
	"""Dit is een commentaar"""
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item)
		else:
			print(each_item)
