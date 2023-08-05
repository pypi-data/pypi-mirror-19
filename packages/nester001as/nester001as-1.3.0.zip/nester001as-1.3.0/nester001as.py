def printListItem(item,indent_status=False,level=0):
	for nest_item in item:
		if isinstance(nest_item,list):
			printListItem(nest_item,indent_status,level+1)
		else:
			if indent_status:
				for tab_stop in range(level):
					print("\t",end='')	
			print(nest_item)
