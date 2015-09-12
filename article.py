#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nico Colic, September 2015

"""Right now, the idea is that Articles have Sections,
   which have Sections
   which have Sentences
   which have Terms and Tokens"""
   
class Unit(object):
	"""Abstract unit for storing tokens, sentences, sections"""
	
	def __init__(self,id_):
		self.subelements = list()
		self.id_ = id_
	
	def tokenise(self,tokeniser=None):
		for subelement in self.subelements:
			subelement.tokenise(tokeniser)
			
	def add_subelement(self,subelement):
		self.subelements.append(subelement)

class Article(Unit):
	"""Stores an article and various subelements for inter-module passing"""
	
	def __init__(self,pmid):
		Unit.__init__(self,pmid)
		
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
		
	def tokenise(self,tokeniser):
		sentences = tokeniser.tokenize_sentences(self.text)
		for sentence in sentences:
			id_ = len(self.subelements)
			self.add_subelement(Sentence(id_,sentence,text))
			
	
	def __init__(self,id_,section_type,text):
		self.type_ = section_type
		self.text = text
		
		Unit.__init__(self,id_)
		
		
class Sentence(Unit):
		
	def __init__(self,id_,text):
		
		
		pass
	
class Token(Unit):
	"""The central unit in this"""
	
	start = None
	end = None
	length = None
	pos = None
	lemma = None
	stem = None
	text = None
	
	def __init__(self):
		pass
		
class Term(Unit):
	
	type_ = None
	subelements = list()
	start = None
	end = None
	length = None
	
	def __init__(self):
		pass
	
	