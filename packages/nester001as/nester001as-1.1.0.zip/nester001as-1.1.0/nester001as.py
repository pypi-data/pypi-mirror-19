def printListItem(item,level=0):
	for nest_item in item:
		if isinstance(nest_item,list):
			printListItem(nest_item,level+1)
		else:
			for tab_stop in range(level):
				print("\t",end='')	
			print(nest_item)
