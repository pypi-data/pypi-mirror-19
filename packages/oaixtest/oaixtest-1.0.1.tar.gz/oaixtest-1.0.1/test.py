#_^@^_ coding: utf-8 _^@^_

def print_list(the_list,indent=False,level=0):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_list(each_item,indent,level+1)
		else:
			if indent:
				for tab_num in range(level):
					print("\t",end='')
			print(each_item)

aa=[1,2,3,[11,22,33,[111,222,333]],"a","b",["aa","bb"]]
print_list(aa,True)
print_list(aa)
