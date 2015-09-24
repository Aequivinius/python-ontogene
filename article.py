#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nico Colic, September 2015

import xml.etree.ElementTree as ET


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
				if subelement.text is not None:
					string += subelement.text + ' '
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
	# example use: my_article.get_sublements(article.Token) from outside, or get.subelements(Token) from inside
	def get_subelements(self,subelement_type):
		
		return_subelements = list()
		
		if self.subelements == None or len(self.subelements) == 0:
			return
		
		if isinstance(self.subelements[0],subelement_type):
			return self.subelements
			
		else:
			for subelement in self.subelements:
				return_subelements.extend(subelement.get_subelements(subelement_type))
		return return_subelements


class Article(Unit):
	
	mesh = None
	type_ = None
	year = None
		
	def __init__(self,id_):
		Unit.__init__(self,id_)
		
		self.mesh = list()
		
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
		
		#             if u'ChemicalList' in pmid_medline:
		#                 chemicals = ET.SubElement(article,'chemicals')
		#                 chemicals.set('id','')
		#                 for chemical in pmid_medline[u'ChemicalList']:
		#                     c = ET.SubElement(chemicals, 'chemical')
		#                     c.set('UI',chemical[u'NameOfSubstance'].attributes[u'UI'])
		#                     c.set('RegistryNumber',chemical[u'RegistryNumber'])
		#                     c.text = chemical[u'NameOfSubstance']
		#             
		#             mesh = ET.SubElement(article,'mesh')
		#             mesh.set('id','')
		#             for mesh_element in pmid_medline[u'MeshHeadingList']:
		#                 m = ET.SubElement(mesh, 'm')
		#                 m.text = mesh_element[u'DescriptorName']
		#                 m.set('UI',mesh_element[u'DescriptorName'].attributes[u'UI'])
		#                 major_topic = mesh_element[u'DescriptorName'].attributes[u'MajorTopicYN']
		#                 m.set('MajorTopicYN',major_topic)
		#             
		#                 qualifier_name = mesh_element[u'QualifierName']
		#                 if qualifier_name != []:
		#                     m.set('qualifier_name',qualifier_name[0])
		#                     m.set('qualifier_name_UI',qualifier_name[0].attributes[u'UI'])
		#                     qualifier_name_major_topic = qualifier_name[0].attributes[u'MajorTopicYN']
		#                     if major_topic != qualifier_name_major_topic:
		#                         m.set('qualifier_name_major_topic',qualifier_name_major_topic)
		#         
		#         except LookupError as error:
		#             print('Tree could not be build, possibly because Pubmed data is in an unexpected format.')
		#             print(error)
		#             return
		#                        

		
	def bioc(self):
		pass
		
	def pickle(self):
		pass
		
	def recognize_entities(self,entity_recognizer=None):
		
		haystack = list()
		sentences = self.get_subelements(Sentence)
		for sentence in sentences:
			sentence_tokens = list()
			tokens = sentence.get_subelements(Token)
			for token in tokens:

				sentence_tokens.append(token.get_tuple())
		haystack.append(sentence_tokens)
		
		# make a list of sentences of lists of tokens with word, start, end
		
		entities = entity_recognizer.recognize_entities(haystack)
		print(entities)
		
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
		tokens = tokenizer.tokenize_words(self.text)
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
				
class Term(Unit):
	
	type_ = None
	subelements = list()
	start = None
	end = None
	length = None
	
	def __init__(self):
		pass
	


#    
#     
#     def export_json(self,output_directory):
#         import json
#         
#         my_directory = self.make_output_subdirectory(output_directory)
# 
#         file_name = os.path.join(my_directory, self.pmid + '.json')
#         with open(file_name,'w') as f:
#             f.write(	json.dumps(self.text[0], indent=2, separators=(',', ':')))
