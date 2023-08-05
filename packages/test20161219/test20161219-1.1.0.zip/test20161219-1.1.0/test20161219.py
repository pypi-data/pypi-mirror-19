""" 循环打印列表"""
def print_lol(the_list,indent = False,level=0):
	for each in the_list:
		#判定是否是一个列表
		if isinstance(each,list):
			print_lol(each,indent,level+1)
		else:
			if indent:
				for tab_stop in range(level):
					print('\t',end='')
			print(each) 
			
		
	