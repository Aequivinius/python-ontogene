#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nico Colic, September 2015

import os.path
import csv
import datetime

class Configuration(object):
	"""Stores and processed configuration for the pipeline. The user only needs to change class variables; the rest can be ignored."""
	
	# VARIABLES TO BE CHANGED BY THE USER
	
	# GENERAL VARIABLES
	# Set to None for silent mode, set to 'CONSOLE' to print to console, set to 'FILE' to print to file
	# In that case, it will print to files in output directory
	verbose = 'FILE'
	# this folder will be used by all modules as output directory. Again, output_directory_mode can be RELATIVE to main.py or ABSOLUTE
	output_directory = 'output'
	output_directory_mode = 'RELATIVE'
	
	# VARIABLES RELATED TO LOADING DATA FROM FILE OR PUBMED
	# Where to load PMIDs from for processing
	# Set pmid_mode to ABSOLUTE or RELATIVE (to main.py) to load from pmids from file
	# Set it to ID to load user_supplied_pmids
	pmid_mode = ''
	pmid_file = 'pmids/test_pmids.txt'
	user_supplied_pmids = [ ]
	
	# this is the email that is used to download from Pubmed.
	pubmed_email = 'ncolic@gmail.com'
	
	# Tokenizers used in text_processing and for entity_recognition
	#	Currently, word_tokenizer can be WordPunctTokenizer or PunktWordTokenizer
	#	sentence_tokenizer currently can only be PunktSentenceTokenizer
	word_tokenizer = 'WordPunctTokenizer'
	sentence_tokenizer = 'PunktSentenceTokenizer'
	
	# VARIABLES RELATED TO ENTITY RECOGNITION
	# List of entities to be used for entity recognition. 
	# termlist_mode can be RELATIVE (to main.py) or ABSOLUTE
	# termlist_format specified number of columns that termlist has. Set to none to detect automatically, this, however, might slow down execution slightly.
	termlist_file = 'entity_recognition/termlists/ontogene_terms_C_D_F03.tsv'
	termlist_mode = 'RELATIVE'
	termlist_format = 6
	
	# COSMETIC VARIABLES
	output_verbose_directory_name = 'verbose'
	
	# INTERNAL VARIABLES
	# These will be overwritten by the constructor
	pmids = list()
	pmid_file_absolute = None
	
	output_directory_absolute = None
	output_verbose_directory_absolute = None
	verbose_file = None
	
	word_tokenizer_object = None
	sentence_tokenizer_object = None
	termlist_file_absolute = None
	
	def __init__(self, user_supplied_pmids=None):
		"""For fast testing, you can use user_supplied_pmids in constructor with a list of PMIDs, rather than changing config file."""
		if user_supplied_pmids:
			self.pmid_mode = 'ID'
			self.user_supplied_pmids = user_supplied_pmids
			
		# check if pmids are strings
		if self.pmid_mode == 'ID':
			self.user_supplied_pmids = [ str(pmid) for pmid in self.user_supplied_pmids ]
				
		self.load_pmids()
		self.make_output_directory()
		
		if self.verbose == 'FILE':
			self.create_verbose_file_names()
		
		self.create_tokenizer_objects()
		self.set_termlist()
			
	
	def load_pmids(self):
		if self.pmid_mode == 'RELATIVE' and self.pmid_file:
			my_directory = os.path.dirname(os.path.abspath(__file__))
			self.pmid_file_absolute = os.path.join(my_directory,self.pmid_file)
			self.load_pmids_from_file()
			
		elif self.pmid_mode == 'ABSOLUTE' and self.pmid_file:
			self.pmid_file_absolute = self.pmid_file
			self.load_pmids_from_file()
		
		elif self.pmid_mode == 'ID' and self.user_supplied_pmids:
			self.pmids = self.user_supplied_pmids
	
	def 	load_pmids_from_file(self):
		with open(self.pmid_file_absolute,'r') as f:
		 	for line in f:
			 	self.pmids.append(line.strip())
			 	
	def make_output_directory(self):
		if self.output_directory_mode == 'RELATIVE':
			my_directory = os.path.dirname(os.path.abspath(__file__))
			self.output_directory_absolute = os.path.join(my_directory, self.output_directory)
		else:
			self.output_directory_absolute = self.output_directory
			
		if not os.path.exists(self.output_directory_absolute):
			try:
				os.makedirs(self.output_directory_absolute)
			except():
				print('Could not create directory ', self.output_directory_absolute)
				return None
	
	def create_tokenizer_objects(self):
		self.create_word_tokenizer_object()
		self.create_sentence_tokenizer_object()	
	
	def create_word_tokenizer_object(self):
		"""Here you can add supported word tokenizers. Note that it must implement the span_tokenize method"""
		if self.word_tokenizer == 'WordPunctTokenizer':
			from nltk.tokenize import WordPunctTokenizer 
			self.word_tokenizer_object = WordPunctTokenizer()
				
		if self.word_tokenizer == 'PunktWordTokenizer':
			from nltk.tokenize import PunktWordTokenizer
			self.word_tokenizer_object = PunktWordTokenizer()
		
	def create_sentence_tokenizer_object(self):
		"""Here you can add supported sentence tokenizers."""
		from nltk.tokenize import PunktSentenceTokenizer
		self.sentence_tokenizer_object = PunktSentenceTokenizer()
		
	def set_termlist(self):
		if self.termlist_mode == 'RELATIVE' and self.termlist_file:
			my_directory = os.path.dirname(os.path.abspath(__file__))
			self.termlist_file_absolute = os.path.join(my_directory,self.termlist_file)
		
		elif self.termlist_mode == 'ABSOLUTE' and self.termlist_file and os.path.exists(self.termlist_file):
				self.termlist_file_absolute = self.termlist_file
		
		else:
			print('No valid termlist provided in config/config.py')
		
		if not self.termlist_format:
			with open(self.termlist_file_absolute) as tsv:
				for line in csv.reader(tsv, delimiter="\t"):
					self.termlist_format = len(line) #this is the first line, then we
					break
	
	def create_verbose_file_names(self):
		
		# verbose subdirectory
		self.output_verbose_directory_absolute = os.path.join(self.output_directory_absolute , self.output_verbose_directory_name )
		if not os.path.exists(self.output_verbose_directory_absolute):
			try:
				os.makedirs(self.output_verbose_directory_absolute)
			except():
				print('Could not create directory ', self.output_verbose_directory_absolute)
				return None
		
		current_date = datetime.datetime.now()
		verbose_file_name = os.path.join(self.output_verbose_directory_absolute,'run_' + str(current_date.day) + '-' + str(current_date.month ) + '-' + str(current_date.year) + '_' + str(current_date.hour) + '-' + str(current_date.minute) + '-' + str(current_date.second) + '.txt' )
		self.verbose_file = open(verbose_file_name,'w')	        
		       