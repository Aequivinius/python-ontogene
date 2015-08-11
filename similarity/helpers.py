#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Helper functions"""



def make_directory(directory):
	import os.path
	
	"""Create folder if it doesn't exist yet"""
	if not os.path.exists(directory):
		try:
			os.makedirs(directory)
			return directory
		except():
			print('Could not create directory ', directory)
			return None
	else:
		return directory
		
def load_termlist_from_pickle(pickle_path):
	import time
	import pickle
	
	terms = dict()
	
	start = time.time()
	print('Loading terms from pickle now')
	
	with open(pickle_path,'rb') as file:
		terms = pickle.load(file)
		
	end = time.time()

	print('Loaded terms from pickle ', end - start)
	return terms