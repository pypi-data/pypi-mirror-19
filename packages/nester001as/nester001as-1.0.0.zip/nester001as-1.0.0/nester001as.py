def printListItem(item):
	for nest_item in item:
		if isinstance(nest_item,list):
			printListItem(nest_item)
		else:
			print(nest_item)
