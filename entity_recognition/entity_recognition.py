#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nico Colic, June 2015

import csv
import time
import pickle
import os.path

class Entity_recognition(object):
	"""Dictionary entity recognition. Object holds dictionary; use my_er.recognise_entities(haystack) which returns list of found entities. The object does not store found entities, so you can use one Entity_recognition object to find NEs in different texts"""
	
	"""Structure of dictionary (called terms): key = first word of term, [ [0] = whole term , [1] = term_id , [2] = term_type , [3] = term_preferred_form, [4] = number of tokens of term ] [ ... ] """
	
	"""Structure of returned entities: key = id, [0] = whole term, [1] - [4] like terms, [5] = start position, [6] = end position"""
	"""Structure of haystack: list of sentences of tuples tuples ([0]: token, [1]: start position in text, [2]: end position in text). This is the format that is produced by Text_processing"""
	
	pickles_directory = 'pickles'
	terms = dict()
	
	def __init__(self, termlist_file_absolute, termlist_format, word_tokenizer,  force_reload=None , pickle_directory=None ):
		"""Loads the terms from file or pickle"""
		"""By default, it will look for a previous pickle by the same name as the termlist_file_absolute. If force_reload is set, it will always load from file. Use this when the file has changed. If loading from file, it will automatically save loaded entities as pickle for faster (up to 20 times) loading the next time."""
		
		"""There are different formats of files to load termlists from: 
			4-tuple (termlist_format=4)
				[0] id, [1] term, [2] type, [3] prefered form
			6-tuple (termlist_format=6)
				[0] original id, [1] term, [2] type, [3] prefered form, [4] resource from which it comes, [5] internal id"""
		
		my_directory = os.path.dirname(os.path.abspath(__file__))		
		termlist_filename = os.path.split(termlist_file_absolute)[1]
		pickles_directory_absolute = os.path.join(my_directory,self.pickles_directory)
		
		# Check if pickle with the same file name exists
		pickle_file = os.path.join(pickles_directory_absolute,termlist_filename) + '.pickle'
		if os.path.exists(pickle_file) and not force_reload:
			print('Found pickle with same name as specified termlist.') 
			print('Set force_reload=1, or delete pickle if you want to load from file.')
			
			self.terms = self.load_termlist_from_pickle(pickle_file)
		
		# Load termlist from file
		else:
			self.terms = self.load_termlist_from_file(termlist_file_absolute,termlist_format,word_tokenizer)
			self.write_terms_to_pickle(self.terms, pickle_file)
							
	def load_termlist_from_pickle(self,pickle_path):
		terms = dict()
		
		start = time.time()
		print('Loading terms from pickle now')
		
		with open(pickle_path,'rb') as file:
			terms = pickle.load(file)
			
		end = time.time()
	
		print('Loaded terms from pickle ', end - start)
		return terms
		
	
		
	def load_termlist_from_file(self,termlist_file, termlist_format, word_tokenizer):
		# Termlist assumed to have the following format:
		# [0] = id, [1] = term to match, [2] = type, [3] = prefered form
		# [0] original id, [1] term, [2] type, [3] prefered form, [4] resource from which it comes, [5] internal id
		
		terms = dict()
		
		start = time.time()
		print("Loading terms from file now.")
		
		with open(termlist_file) as tsv:
			for line in csv.reader(tsv, delimiter="\t"):
								
				term_id = line[0] if termlist_format==4 else line[5]
				term_resource = line[4] if termlist_format==6 else 'unknown'
				term_original_id = line[0]
				
				term = word_tokenizer.tokenize(line[1].lower())
				term_type = line[2]
				term_preferred_form = line[3]
				
				value_tuple = ( term , term_id , term_type , term_preferred_form , len(term) , term_resource , term_original_id )
				
				if term[0] in terms :
					terms[term[0]].append(value_tuple)
				else :
					terms[term[0]] = [ value_tuple ]
		end = time.time()
		print("Finished loading dictionary in ", round(end - start,2), " seconds")
		
		return terms
	
	def write_terms_to_pickle(self,terms,filename):
		if not os.path.exists(os.path.dirname(filename)):
			os.makedirs(os.path.dirname(filename))
		
		with open(filename,'wb') as file:
			pickle.dump(terms,file)
		print('Written terms to pickle at ', filename)
	
	def recognize_entities(self,sentences):
		"""Will go through the words and try to match them to the terms"""
		"""Words is expected in this format: (word, start position, end position)"""
		"""Returns a list of found entities"""
		
		entities = list()
		
		entity_id = -1
		
		for words in sentences:
			# using a C-style loop for easy peeking at words following the current one
			for i in range(len(words)):
				
				word = words[i][0].lower()
				if word in self.terms:
									
					entity_id = entity_id + 1
					
					# check if multiple entries for first word in terms
					
					for entry in self.terms[word]:
											
						# remember, entry[4] is the number of words the NE has
						# so if it is > 1, we have a multi-word entry and we loop through every word
						if entry[4] > 1:
							matched = True
							match_length = 0
							
							# entry[0] is the list of tokens in the multi-word NE
							for j in range(len(entry[0])):
								if not matched :
									break
								
								if i+j > ( len(words) - 1 ) :
									matched = False
									break
									
								if entry[0][j] != words[i+j][0]:
									matched = False
								else:
									match_length = match_length + len(entry[0][j])
							
							if matched:
								entities.append( ( entry[0] , entry[1] , entry[2] , entry[3] , entry[4] , words[i][1] , words[i+j-1][2]))
								# TODO: one could also set i to skip the words so far identified as a multi-word entry. But this might lead to some nested / parallel multi-word NEs to be missed
						
						else:
						# else it's a single word NE that was found	
							entities.append( ( entry[0] , entry[1] , entry[2] , entry[3] , entry[4] , words[i][1] , words[i][2] ) )
			
		return entities
		
	def export_tsv(self, id, entities, output_directory):
		
		my_directory = self.make_output_subdirectory(output_directory)		
		my_file = os.path.join(my_directory, id + '.tsv')
		
		with open(my_file,'w') as f:
			writer = csv.writer(f, delimiter='\t')
			for entity in entities:
				writer.writerow(entity)
		
	def export_tsv_legacy_format(self, id, entities, output_directory):
		
		my_directory = self.make_output_subdirectory(output_directory)		
		my_file = os.path.join(my_directory, id + '.tsv')
		
		with open(my_file,'w') as f:
			writer = csv.writer(f, delimiter='\t')
			writer.writerow(['DOCUMENT ID', 'TYPE' , 'START POSITION' , 'END POSITION' , 'MATCHED TERM' , 'PREFERRED FORM' , 'TERM ID' , 'ORIGIN WITHIN DOCUMENT' , 'SENTENCE'])
			for entity in entities:
				
				matched_term = ' '.join(entity[0])
				row = [ id , entity[2] , entity[5] , entity[6] , matched_term , entity[3] , entity[1] , 'origin' , 'sentence']
				
				writer.writerow(row)	
			
	def make_output_subdirectory(self,output_directory):
		my_directory = os.path.join(output_directory, 'entity_recognition')
		return self.make_directory(my_directory)
							
	def make_directory(self,directory):
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
