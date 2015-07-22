#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path


class Configuration(object):
	"""Stores and processed configuration for the pipeline. The user only needs to change class variables; the rest can be ignored."""
	
	# VARIABLES TO BE CHANGED BY THE USER
	
	# Where to load PMIDs from for processing
	# Set pmid_mode to ABSOLUTE or RELATIVE (to control.py) to load from pmid_file
	# Set it to ID to load user_supplied_pmids, which is a list of strings
	pmid_mode = 'RELATIVE'
	pmid_file = 'pmids/test_pmids.txt'
	user_supplied_pmids = [ '11111111' ]
	
	# this is the email that is used to download from Pubmed.
	pubmed_email = 'ncolic@gmail.com'
	
	# this folder will be used by all modules as output directory. Again, output_directory_mode can be RELATIVE to control.py or ABSOLUTE
	output_directory = 'output'
	output_directory_mode = 'RELATIVE'

	# Tokenizer used in text_processing and for entity_recognition
	tokenizer = 'WordPunctTokenizer'
	
	# INTERNAL VARIABLES
	# These will be overwritten by the constructor
	pmids = list()
	pmid_file_absolute = None
	output_directory_absolute = None

	
	def __init__(self, user_supplied_pmids=None):
		"""For fast testing, you can user user_supplied_pmids in constructor with a list of strings, rather than changing config file."""
		if user_supplied_pmids:
			self.pmid_mode = 'ID'
			self.user_supplied_pmids = user_supplied_pmids
		
		self.load_pmids()
		self.make_output_directory()
			
	
	def load_pmids(self):
		if self.pmid_mode == 'RELATIVE' and self.pmid_file:
			my_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			self.pmid_file_absolute = os.path.join(my_directory,self.pmid_file)
			self.load_pmids_from_file()
			
		elif self.pmid_mode == 'ABSOLUTE' and self.pmid_file:
			self.pmid_file_absolute = self.pmid_file
			self.load_pmids_from_file()
		
		elif self.pmid_mode == 'ID' and self.user_supplied_pmids:
			self.pmids = self.user_supplied_pmids
			
		else:
			print('Make sure you set pmid_mode in config.py correctly')
			quit()
	
	def 	load_pmids_from_file(self):
		with open(self.pmid_file_absolute,'r') as f:
		 	for line in f:
			 	self.pmids.append(line.strip())
			 	
	def make_output_directory(self):
		if self.output_directory_mode == 'RELATIVE':
			my_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			self.output_directory_absolute = os.path.join(my_directory, self.output_directory)
		else:
			self.output_directory_absolute = self.output_directory
			
		if not os.path.exists(self.output_directory_absolute):
			try:
				os.makedirs(self.output_directory_absolute)
			except():
				print('Could not create directory ', absolute_output_directory)
				return None
	        
		       