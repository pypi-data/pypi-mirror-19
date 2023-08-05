def printListItem(item,indent_status=False,level=0,fh=sys.stdout):
	for nest_item in item:
		if isinstance(nest_item,list):
			printListItem(nest_item,indent_status,level+1,fh=sys.stdout)
		else:
			if indent_status:
				for tab_stop in range(level):
					print("\t",end='',file=fh)	
			print(nest_item,file=fh)
