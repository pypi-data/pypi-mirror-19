#!/usr/bin/env python
#-*- coding=utf-8 -*-

def print_lol(the_list):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item)
		else:
			print(each_item)
			
# movies = ["The Holy Grail",1975,"Terry Jones & Terry Gilliam",91,["Graham Chapman", ["Michael Palin", "Jonn Cleese","Terry Gilliam","Eric Idle"]]]
#
# print_lol(movies)


