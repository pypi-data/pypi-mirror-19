#!/usr/bin/env python
#-*- coding=utf-8 -*-

import sys
'''
模块提供了一个print_lol()函数，用来打印列表
'''
def print_lol(the_list,indent=False,level=0,fh=sys.stdout):
	'''
	打印列表，列表中各项会打印到屏幕上，可以选择是否实现缩进效果
	:param the_list: the_list 任何python列表，可以有嵌套列表
	:param indent: indent 是否打开缩进功能，默认为不打开False，打开为True
	:param level: level 从什么位置开始缩进，默认为从0开始，只有当indent=True时level才有效
	:return: 打印列表
	'''
	for each_item in the_list:
		if isinstance(each_item,list):#判断list
			print_lol(each_item,indent,level+1,fh)
		else:
			if indent:
				for tab_stop in range(level):
					print("\t",end='',file=fh)#在屏幕上实现缩进
			print(each_item,file=fh)


'''
将每一个字符串中的'-'和':'换成'.'，使得时间表达的方式统一
'''
def sanitize(time_string):
	if '-' in time_string:
		splitter = '-'
	elif ':' in time_string:
		splitter = ':'
	else:
		return(time_string)

	(mins, secs) = time_string.split(splitter)
	return(mins +'.' +secs)





