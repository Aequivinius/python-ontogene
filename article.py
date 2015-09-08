#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nico Colic, September 2015

"""Right now, the idea is that Articles have Sections,
   which have Sections
   which have Sentences
   which have Terms and Tokens"""

class Article(object):
	"""Stores an article and various subelements for inter-module passing"""
	
	# may or may not have a PMID
	id_ = None
	subelements = list()
	meta = None
	
	# add some recursive shit, that finds terms for example?
	
	def __init__(self,pmid):
		id_ = pmid
		
	def add_section(self,section_type,text):
		self.subelements.append(Section(section_type,text))
		
	def xml(self):
		pass
		
	def bioc(self):
		pass
		
	def pickle(self):
		pass
		
class Section(object):
	"""Can be something like title or abstract"""
	
	id_ = None
	type_ = None
	text = None
	subelements = list()
	
	def __init__(self,section_type,text):
		self.type_ = section_type
		self.text = text
		
class Sentence(object):
	
	id_ = None
	subelements = list()
	
	def __init__(self):
		pass
	
class Token(object):
	"""The central unit in this"""
	
	id_ = None
	start = None
	end = None
	length = None
	pos = None
	lemma = None
	stem = None
	text = None
	
	def __init__(self):
		pass
		
class Term(object):
	
	id_ = None
	type_ = None
	subelements = list()
	start = None
	end = None
	length = None
	
	def __init__(self):
		pass
	
	