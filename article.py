#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nico Colic, September 2015

import xml.etree.ElementTree as ET
import pickle


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
		self.id_ = id_
	
	# Used so you can print(my_article), for example
	# Useful for testing (but use xml() etc for true outputting)
	def __repr__(self):
		string = ''
		if self.subelements == None or len(self.subelements) == 0:
			return self.text
		
		for subelement in self.subelements:
			if hasattr(subelement,'text'):
				if subelement.text is not None:
					string += subelement.text + ' '
			else:
				string += subelement.__repr__()
		
		# get rid of final \n	
		return string[:-1]

	
	# Just calls tokenize() in all subelements
	# The classes that actually tokenize overwrite this function
	# This allows for a flexible hierarchy
	# Note that no class actually tokenizes
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
		if not subelement.id_:
			# subelement has not yet been added to the subelements list
			generated_id = len(self.subelements)
			subelement.id_ = generated_id
			
		self.subelements.append(subelement)
		
	def get_subelements(self,subelement_type):
		"""returns a list of subelements of the supplied type without knowing the hierarchy"""
		"""example use: my_article.get_sublements(article.Token) from outside, or get.subelements(Token) from within the class"""
		
		return_subelements = list()
		
		if self.subelements == None or len(self.subelements) == 0:
			return
		
		if isinstance(self.subelements[0],subelement_type):
			return self.subelements
			
		else:
			for subelement in self.subelements:
				return_subelements.extend(subelement.get_subelements(subelement_type))
		return return_subelements

###################################
# actual classes begin here #######
###################################

class Article(Unit):
	
	mesh = None
	type_ = None
	year = None
		
	def __init__(self,id_):
		Unit.__init__(self,id_)
		
		self.mesh = list()
		self.entities = list()
		
	def add_section(self,section_type,text):
		id_ = len(self.subelements)
		self.add_subelement(Section(id_,section_type,text))
		
	def set_mesh(self,mesh):
		"""Expects lists of strings"""
		self.mesh = mesh
	
	def print_xml(self,output_file,pretty_print=None):
		article = self.xml()
		
		# write using etree
		if not pretty_print:
			with open(output_file,'wb') as f:
			    ET.ElementTree(article).write(f,encoding="UTF-8",xml_declaration=True)
		
		# Pretty Print
		if pretty_print:
			from xml.dom import minidom
			
			pretty_article = minidom.parseString(ET.tostring(article, 'utf-8')).toprettyxml(indent="	")
			with open(output_file,'w') as f:
			    f.write(pretty_article)
						
	def xml(self):
		"""This structure is build recursively, so all subordinate classes implement it, too"""
		
		article = ET.Element('article')
		article.set('id',self.id_)
		
		if self.year != None:
			article.set('year',self.year)
		if self.type_ != None:
			article.set('type',self.type_)
		
		for subelement in self.subelements:
			subelement.xml(article)
		
		return article
	
	def bioc(self):
		pass
		
	def json(self):
		pass
		
		
		#     def export_json(self,output_directory):
		#         import json
		#         
		#         my_directory = self.make_output_subdirectory(output_directory)
		# 
		#         file_name = os.path.join(my_directory, self.pmid + '.json')
		#         with open(file_name,'w') as f:
		#             f.write(	json.dumps(self.text[0], indent=2, separators=(',', ':')))
		
	def pickle(self,output_file):
		with open(output_file,'wb') as f:
			pickle.dump(self,f)
	
	@classmethod
	def unpickle(cls, input_file):
		"""Use as my_article = article.Article.unpickle(path)"""
		with open(input_file,'rb') as f:
			return pickle.load(f)
		
	def recognize_entities(self,entity_recognizer):
		# entity_recognizer.recognize entities() requires sentence tokens
		haystack = self.get_sentence_tokens()
		entities = entity_recognizer.recognize_entities(haystack)
		for entity in entities:
			my_entity = Entity(	id_= len(self.entities) ,
								text = ' '.join(entity[0]),
								text_tokens = entity[0],
								start=entity[1],
								end=entity[2],
								type_=entity[3],
								prefered_form=entity[4],
								origin_db=entity[5],
								origin_id=entity[6] )
			
			self.entities.append(my_entity)
	
	def print_entities_xml(self,output_file,pretty_print=None):
		entities = self.entities_xml()
		
		# write using etree
		if not pretty_print:
			with open(output_file,'wb') as f:
				ET.ElementTree(entities).write(f,encoding="UTF-8",xml_declaration=True)
		
		# Pretty Print
		if pretty_print:
			from xml.dom import minidom
			
			pretty_article = minidom.parseString(ET.tostring(entities, 'utf-8')).toprettyxml(indent="	")
			with open(output_file,'w') as f:
				f.write(pretty_article)
	
	def entities_xml(self):
		entities = ET.Element('entities')
		entities.set('article_id',str(self.id_))
		
		for entity in self.entities:
			entity.xml(entities)
		
		return entities
	
	def get_sentence_tokens(self):
		"""Returns a list of sentences, each of which is a list of tokens in the following format:
		   (word, start position, end position)"""
		return_list = list()
		sentences = self.get_subelements(Sentence)
		for sentence in sentences:
			sentence_tokens = list()
			tokens = sentence.get_subelements(Token)
			for token in tokens:
				sentence_tokens.append(token.get_tuple())
			return_list.append(sentence_tokens)
		return return_list
		
	# This is only used to compare output to old pipeline
	def export_tsv_legacy_format(self, output_file):
		import csv
		with open(output_file,'w') as f:
			writer = csv.writer(f, delimiter='\t')
			writer.writerow(['DOCUMENT ID', 'TYPE' , 'START POSITION' , 'END POSITION' , 'MATCHED TERM' , 'PREFERED FORM' , 'TERM ID' , 'ORIGIN WITHIN DOCUMENT' , 'SENTENCE'])
			for entity in self.entities:
				row = [ self.id_ , entity.type_ , entity.start , entity.end , entity.text , entity.prefered_form , entity.origin_id , 'origin' , 'sentence']
				
				writer.writerow(row)

	
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
				
	def xml(self,parent):
		section = ET.SubElement(parent,'section')
		section.set('id',str(self.id_))
		section.set('type',self.type_)
		
		if self.subelements == None:
			section.text = self.text
		
		for subelement in self.subelements:
			subelement.xml(section)
				
class Sentence(Unit):
	
	text = None
		
	def __init__(self,id_,text):
		self.text = text
		
		Unit.__init__(self,id_)
		
	def tokenize(self,tokenizer):
		tokens = tokenizer.span_tokenize_words(self.text)
		tokens = tokenizer.flatify(tokens)
		for token in tokens:
			id_ = len(self.subelements)
			self.add_subelement(Token(id_,token[0],token[1],token[2]))
			
	def xml(self,parent):
		sentence = ET.SubElement(parent,'sentence')
		sentence.set('id',str(self.id_))
		
		if self.subelements == None:
			sentence.text = self.text
			
		for subelement in self.subelements:
			subelement.xml(sentence)
	
class Token(Unit):
	"""The central unit in this"""
	
	start = None
	end = None
	length = None
	pos = None
	lemma = None
	stem = None
	text = None
	
	def __init__(self,id_,text,start,end):
		self.text = text
		self.start = start
		self.end = end
		self.length = end - start
		Unit.__init__(self,id_)
	
	def xml(self,parent):
		token = ET.SubElement(parent,'token')
		token.set('id',str(self.id_))
		token.set('start',str(self.start))
		token.set('end',str(self.end))
		token.set('length',str(self.length))
		token.text = self.text
		
	def get_tuple(self):
		return (self.text, self.start, self.end)
				
class Entity(Unit):
	
	type_ = None
	start = None
	end = None
	length = None
	text = None
	
	def __init__(self,	id_,
						start,
						end,
						text=None,
						text_tokens=None,
						type_=None,
						prefered_form=None,
						origin_db=None,
						origin_id=None ):
		
		self.subelements = text_tokens
		self.text_tokens = text_tokens
		self.type_ = type_
		self.start = start
		self.end = end
		self.origin_db = origin_db
		self.origin_id= origin_id
		self.prefered_form=prefered_form
		self.text = text
		
		if not text and text_tokens:
			self.text = ' '.join(text_tokens)
		
		Unit.__init__(self,id_)
		
	def xml(self,parent):
		entity = ET.SubElement(parent,'entity')
		entity.set('id',str(self.id_))
		entity.set('type',self.type_)
		entity.set('start',str(self.start))
		entity.set('end',str(self.end))
		entity.set('origin_db',self.origin_db)
		entity.set('origin_id',str(self.origin_id))
		entity.set('prefered_form',self.prefered_form)
		
		if self.text_tokens:
			for text_token in self.text_tokens:
				xml_token = ET.SubElement(entity,'token')
				xml_token.text = text_token
		elif self.text:
			entity.text = self.text

		return entity
