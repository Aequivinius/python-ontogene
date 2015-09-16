#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nico Colic, September 2015

"""Used for inter-module communication. Stores articles in various stages of processing. Designed to be flexible in regards to hierarchy."""
"""For example, while it is assumed that normally articles have sections, this is not necessary."""
   
class Unit(object):
	"""Abstract unit which implements functions which are used by all structures"""
	
	sublements = None
	id_ = None
	
	# Mainly initialises subelements list
	def __init__(self,id_):
		
		# having two lists allows to preserve order
		self.subelements = list()
		self.subelements_ids = list()
		self.id_ = id_
	
	# Used so you can print(my_article), for example
	# Useful for testing (but use xml() etc for true outputting)
	def __repr__(self):
		string = ''
		for subelement in self.subelements:
			if hasattr(subelement,'text'):
				string += subelement.text + '\n'
			else:
				string += subelement.__repr__()
		
		# get rid of final \n	
		return string[:-1]

	
	# Just calls tokenize() in all subelements
	# The classes that actually tokenize overwrite this function
	# This allows for a flexible hierarchy
	# Note that it is expected that the no class of the article module actually tokenizes, 
	# rather they will call a tokenize()-function on the tokenizer object
	def tokenize(self,tokenizer):
		for subelement in self.subelements:
			subelement.tokenize(tokenizer)
	
	def add_subelement(self,subelement,id_=None):
		
		# Checks that all elements in the subelements list are of the same type
		if len(self.subelements) > 0:
			if not type(self.subelements[0] == type(subelement)):
				raise TypeError("Subelements list should only contain objects of same type")
				return
		
		# if id_ in subelement is set, we use it
		# otherwise we create a new id_
		try:
			self.subelements_ids.append(subelement.id_)
		except AttributeError:
			# subelement has not yet been added to the subelements list
			generated_id = len(self.subelements)
			self.subelements_ids.append(generated_id)
			subelement.id_ = generated_id
			
		self.subelements.append(subelement)
		
	# returns a list of subelements of the supplied type without knowing the hierarchy
	# example use: my_article.get_sublements(article.Token)
	def get_subelements(self,subelement_type):
		
		return_subelements = list()
		
		if len(self.subelements) == 0:
			return
		
		print(type(self.subelements[0]),subelement_type)
		if isinstance(self.subelements[0],subelement_type):
			print("in here")
			return self.subelements
			
		else:
			for subelement in self.subelements:
				return_subelements.append(subelement.get_subelements(subelement_type))
				
		return return_subelements
			

class Article(Unit):
		
	def __init__(self,id_):
		Unit.__init__(self,id_)
		
	def add_section(self,section_type,text):
		id_ = len(self.subelements)
		self.add_subelement(Section(id_,section_type,text))
		
	def xml(self):
		pass
		
	def bioc(self):
		pass
		
	def pickle(self):
		pass
		
class Section(Unit):
	"""Can be something like title or abstract"""
	
	type_ = None
	text = None
	
	def __init__(self,id_,section_type,text):
		self.type_ = section_type
		self.text = text
		
		Unit.__init__(self,id_)
		
	def tokenize(self,tokenizer):
		sentences = tokenizer.tokenize_sentences(self.text)
		for sentence in sentences:
			id_ = len(self.subelements)
			self.add_subelement(Sentence(id_,sentence))
			
			for subelement in self.subelements:
				subelement.tokenize(tokenizer)
			
class Sentence(Unit):
	
	text = None
		
	def __init__(self,id_,text):
		self.text = text
		
		Unit.__init__(self,id_)
		
	def tokenize(self,tokenizer):
		tokens = tokenizer.tokenize_words(self.text)
		print(tokens)
		for token in tokens:
			id_ = len(self.subelements)
			self.add_subelement(Token(id_,token[0]))
	
class Token(Unit):
	"""The central unit in this"""
	
	start = None
	end = None
	length = None
	pos = None
	lemma = None
	stem = None
	text = None
	
	def __init__(self,id_,text):
		Unit.__init__(self,id_)
		
class Term(Unit):
	
	type_ = None
	subelements = list()
	start = None
	end = None
	length = None
	
	def __init__(self):
		pass
	
	