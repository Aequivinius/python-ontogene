#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nico Colic, September 2015

import csv
import time
import pickle
import os.path

class Entity_recognition(object):
	"""Dictionary entity recognition. Object holds dictionary (called terms), so it has to be loaded only once. Use object.recognize_entities(haystack), which returns a list of entities"""
	
	# This is the default folder in which we check for files, relative to this entity_recognition.py. Use the pickle_directory variable in the constructor to change this to a different directory
	pickles_directory = 'pickles'
	terms = dict()
	verbose = None
	
	def __init__(self, 	termlist_file_absolute, 
						termlist_format, 
						word_tokenizer, 
						
						force_reload = None , 
						pickle_directory = None , 
						verbose = None , 
						verbose_file = None ):
		"""Loads the terms from file or pickle"""
		
		"""If you load from file, you need to supply a word_tokenizer which implements the tokenize_words() function. Ideally, this is the same tokenizer that you use to tokenize the text in which you want to find entities."""
		
		"""By default, it will first look for a pickle with the same name as the termlist_file_absolute. If force_reload is set, it will load from file in anycase. Use this when the file has changed. If loading from file, it will automatically save loaded entities as pickle for faster (up to 20 times) loading the next time."""
		
		# Find out various paths used to check for presence of files
		my_directory = os.path.dirname(os.path.abspath(__file__))		
		termlist_filename = os.path.split(termlist_file_absolute)[1]
		pickles_directory_absolute = os.path.join(my_directory,self.pickles_directory)
		
		# verbose 
		if verbose and verbose_file:
			self.verbose = verbose
			self.verbose_file = verbose_file
		
		# Check if pickle with the same file name exists
		pickle_file = os.path.join(pickles_directory_absolute,termlist_filename) + '.pickle'
		if os.path.exists(pickle_file) and not force_reload:
			self.terms = self.load_termlist_from_pickle(pickle_file)
			
		# Load termlist from file
		else:
			self.terms = self.load_termlist_from_file(termlist_file_absolute,termlist_format,word_tokenizer)
			self.write_terms_to_pickle(self.terms, pickle_file)
	
	# After dictionary has been loaded from file, it will have the following internal structure: 
	# key = first word of term, [ 
	#	[0] = whole term , 
	# 	[1] = term_id (in the respective database), 
	# 	[2] = term_type (or category), 
	# 	[3] = term_preferred_form , 
	# 	[4] = number of tokens of term (this speeds up search)
	#	[5] = resource of origin
	#	[6] = original ID
	# ] 
							
	def load_termlist_from_pickle(self, pickle_path ):
		terms = dict()
		
		if self.verbose:
			start = time.time()
			
			if self.verbose == 'CONSOLE':
				print('Found pickle with same name as specified termlist.') 
				print('Set force_reload=1, or delete pickle if you want to load from file.')
				print('Loading terms from pickle now')
			if self.verbose == 'FILE':
				pass
		
		with open(pickle_path,'rb') as file:
			terms = pickle.load(file)
			
		if self.verbose:
			end = time.time()
			
			if self.verbose == 'CONSOLE':
				print('Loaded terms from pickle in ', end - start , ' seconds')
			if self.verbose == 'FILE':
				self.verbose_file.write('Loaded terms from pickle at '+ str(start) + ' in ' + str(end - start) + ' seconds\n')
			
		return terms
		
	def load_termlist_from_file( self,termlist_file, termlist_format, word_tokenizer ):
		"""There are different formats of files to load termlists from: 
		4-tuple (termlist_format=4)
			[0] id, [1] term, [2] type, [3] prefered form
		
		6-tuple (termlist_format=6)
			[0] original id, [1] term, [2] type, [3] prefered form, [4] resource from which it comes, [5] internal id"""
		
		terms = dict()
		
		if self.verbose:
			start = time.time()
			
			if self.verbose == 'CONSOLE':
				print("Loading terms from file now.")
		
		with open(termlist_file) as tsv:
			for line in csv.reader(tsv, delimiter="\t"):
								
				term_id = line[0] if termlist_format==4 else line[5]
				term_resource = line[4] if termlist_format==6 else 'unknown'
				term_original_id = line[0]
				
				term = word_tokenizer.tokenize_words(line[1].lower())
				term_type = line[2]
				term_preferred_form = line[3]
				
				value_tuple = ( term , term_id , term_type , term_preferred_form , len(term) , term_resource , term_original_id )
				
				if term[0] in terms :
					terms[term[0]].append(value_tuple)
				else :
					terms[term[0]] = [ value_tuple ]
					
		if self.verbose:
			end = time.time()
			
			if self.verbose == 'CONSOLE':
				print("Finished loading dictionary in ", round(end - start,2), " seconds")
			
			if self.verbose == 'FILE':
				self.verbose_file.write('Loaded dictionary from file at ' + str(start) + ' in ' + str(end-start) + ' seconds\n')
		
		return terms
	
	def write_terms_to_pickle(self,terms,filename):
		if not os.path.exists(os.path.dirname(filename)):
			os.makedirs(os.path.dirname(filename))
		
		with open(filename,'wb') as file:
			pickle.dump(terms,file)
			
		if self.verbose == 'CONSOLE':
			print('Written terms to pickle at ', filename)
			
		if self.verbose == 'FILE':
			self.verbose_file.write('Written terms to pickle at ' + filename + ' at ' + str(time.time()) + '\n')
	
	def recognize_entities(self,sentences):
		"""Will go through the words and try to match them to the terms"""
		
		"""Sentences is expected in this format: [ [ (word, start position, end position)][ words of next sentence ] [ ... ] ]"""
		
		"""Returns a list of found entities: 
			[0] whole term
			[1] start position
			[2] end position
			
			[3] type
			[4] prefered form
			[5] resource from which it comes
			[6] internal id
			
			* [5] and [6] are only used if using termlist_format=6"""
		
		entities = list()
		entity_id = -1
		
		if self.verbose:
			start = time.time()
				
		for words in sentences:
			
			# using a C-style loop for easy peeking at words following the current one
			# looping through the words of sentence
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
								#                  whole term start         end               type       prefered   origin     internal id  
								entities.append( ( entry[0] , words[i][1] , words[i+j-1][2] , entry[2] , entry[3] , entry[5] , entry[6] ) )								
								# one could also set i to skip the words so far identified as a multi-word entry. But this might lead to some nested / parallel multi-word NEs to be missed
						else:
							# else it's a single word NE that was found
							#                  whole term start         end           type       prefered   origin     internal id  
							entities.append( ( entry[0] , words[i][1] , words[i][2] , entry[2] , entry[3] , entry[5] , entry[6] ) )
														
		if self.verbose:
			end = time.time()
			if self.verbose == 'CONSOLE':
				print('Found ' + str(len(entities)) + ' entities in text in ' + str(end-start) + ' seconds')
			if self.verbose == 'FILE':
				self.verbose_file.write('Found ' + str(len(entities)) + ' entities in text at ' + str(time.time()) + ' in ' + str(end-start) + ' seconds\n')
			
		return entities		
	
	# these functions are here to allow using the module independently, in which case you do:
	#	my_er = entitiy_recognition(...)
	#	entities = my_er.recognize_entities(...)
	#	my_er.export_tsv(entities,output)
	# Note thought that the Article class offers more export possibilities
	def export_tsv(self, entities, output_file):
		
		with open(output_file,'w') as f:
			writer = csv.writer(f, delimiter='\t')
			for entity in entities:
				writer.writerow(entity)
	
	# Since the ER class doesn't know where the texts come from, it cannot set the fields ORIGIN WITHIN DOCUMENT and SENTENCE; as well as not use the proper IDs for the entities, these are set by the Article class
	# For this, use export functions of article class
	def export_tsv_legacy_format(self, document_id, entities, output_file):
		with open(output_file,'w') as f:
			writer = csv.writer(f, delimiter='\t')
			writer.writerow(['DOCUMENT ID', 'TYPE' , 'START POSITION' , 'END POSITION' , 'MATCHED TERM' , 'PREFERED FORM' , 'TERM ID' , 'ORIGIN WITHIN DOCUMENT' , 'SENTENCE'])
			for entity in entities:
				matched_term = ' '.join(entity[0])
				row = [ document_id , entity[3] , entity[1] , entity[2] , matched_term , entity[4] , entity[6] , 'origin' , 'sentence']
				
				writer.writerow(row)