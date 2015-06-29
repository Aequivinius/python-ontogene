#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nico Colic, June 2015

import csv
from nltk.tokenize import WordPunctTokenizer
import time
import pickle
import os.path

class Entity_recognition(object):
	"""Allows list-based entity recognition for a piece of text"""
	"""The object holds the list of entities to be recognised. To find entities, use my_er.recognise_entities(haystack_words), which will return a list of found entities"""
	"""Consequently, the object does not store the found entities. This is done so that you can use one Entity_recognition object to find NEs in different texts without having to load the termlist anew everytime. That also means that you have to deal with the found entities in the control.py file."""
	
	"""Structure of terms: key = first word of term, [0] = whole term , [1] = term_id , [2] = term_type , [3] = term_preferred_form, [4] = number of tokens of term"""
	"""Structure of returned entities: key = id, [0] = whole term, [1] - [4] like terms, [5] = start position, [6] = end position"""
	"""Structure of words (supplied to find NEs in): [0]: token, [1]: start position in text, [2]: end position in text"""
	
	default_termlist = 'ctd.csv'
	terms = dict()
	
	def __init__(self, termlist_path=None, force_reload=None, tokenizer='WordPunctTokenizer'):
		"""Loads the terms from file or pickle"""
		"""By default, it will look for a previous pickle by the same name as the termlist_path. If force_reload is set, it will always load from file. Use this when the file has changed. If loading from file, it will automatically save loaded entities as pickle for faster (up to 20 times) loading the next time."""
		
		my_path = os.path.dirname(os.path.abspath(__file__))
		
		# Check if user has specified a termlist to load, otherwise load default
		if not termlist_path :
			termlist_path = os.path.join(my_path,self.default_termlist)
		
		termlist_filename = os.path.split(termlist_path)[1]
		pickles_path = os.path.join(my_path,'pickles')
		
		# Check if pickle with the same file name exists
		pickle_path = os.path.join(pickles_path,termlist_filename) + '.pickle'
		if os.path.exists(pickle_path) and not force_reload:
			print('Found pickle with same name as specified termlist.') 
			print('Set force_reload=1, or delete pickle if you want to load from file.')
			
			self.terms = self.load_termlist_from_pickle(pickle_path)
		
		# Load termlist from file
		else:
			print(termlist_path)
			self.terms = self.load_termlist_from_file(termlist_path,tokenizer)
			self.write_terms_to_pickle(self.terms, pickle_path)
						
	def load_termlist_from_pickle(self,pickle_path):
		terms = dict()
		
		start = time.time()
		print('Loading terms from pickle now')
		
		with open(pickle_path,'rb') as file:
			terms = pickle.load(file)
			
		end = time.time()
	
		print('Loaded terms from pickle ', end - start)
		return terms
		
	def load_termlist_from_file(self,termlist_path,tokenizer):
		# Termlist assumed to have the following format:
		# [0] = id, [1] = term to match, [2] = type, [3] = prefered form
		
		terms = dict()
		word_tokenizer = None
		
		# Add other supported tokenizers here
		if tokenizer == 'WordPunctTokenizer':
			word_tokenizer = WordPunctTokenizer()
		
		if tokenizer == 'PunktWordTokenizer':
			from nltk.tokenize import PunktWordTokenizer
			word_tokenizer = PunktWordTokenizer()
			
		if not tokenizer:
			print(tokenizer, " you specified is not supported. Use default option or add in Text_processing.__init__(). Using default WordPunctTokenizer.")
			word_tokenizer = WordPunctTokenizer()
		
		start = time.time()
		print("Loading terms from file now.")
		
		with open(termlist_path) as tsv:
			for line in csv.reader(tsv, delimiter="\t"):
								
				term_id = line[0]
				
				term = word_tokenizer.tokenize(line[1])
				term_type = line[2]
				term_preferred_form = line[3]
				
				value_tuple = ( term , term_id , term_type , term_preferred_form , len(term) )
				
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
	
	def recognise_entities(self,words,terms=None):
		"""Will go through the words and try to match them to the terms"""
		"""Words is expected in this format: (word, start position, end position)"""
		"""Returns a list of found entities"""
		
		entities = list()
		
		if not terms:
			terms = self.terms
		
		entity_id = -1
		
		# using a C-style loop for easy peeking at words following the current one
		for i in range(len(words)):
			
			word = words[i][0]
			if word in terms:
								
				entity_id = entity_id + 1
				
				# check if multiple entries for first word in terms
				for entry in terms[word]:
										
					# remember, entry[4] is the number of words the NE has
					# so if it is > 1, we have a multi-word entry and we loop through every word
					if entry[4] > 1:
						matched = True
						match_length = 0
						
						# entry[0] is the list of tokens in the multi-word NE
						for j in range(len(entry[0])):
							if not matched:
								break
							if matched and i+j < len(words) and entry[0][j] != words[i+j][0]:
								matched = False
							else:
								match_length = match_length + len(entry[0][j])
								# TODO: like this we have an inefficiency because we check for all the entries, even though we could save ourselves some work if they we're structured like a tree
						
						if matched:
							entities.append( ( entry[0] , entry[1] , entry[2] , entry[3] , entry[4] , words[i][1] , words[i+j][2]))
							# TODO: one could also set i to skip the words so far identified as a multi-word entry. But this might lead to some nested / parallel multi-word NEs to be missed
					
					else:
					# else it's a single word NE that was found	
						entities.append( ( entry[0] , entry[1] , entry[2] , entry[3] , entry[4] , words[i][1] , words[i][2] ) )
		
		return entities
		
# TODO: write export functions for found entities
