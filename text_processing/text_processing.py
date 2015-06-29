#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nico Colic, June 2015

import nltk

class Text_processing(object):
	"""Allows to do tokenisation and PoS tagging on a given text"""
	
	"""For now, needs manual downloading in NLTK of tokenizers/punkt and maxent_treebank_pos_tagger before it works"""
	
	def __init__(self, text, text_id):
		
		# TODO: this code fragment should automatically download nltk models if they haven't been downloaded yet,
		# but it doesn't seem to work. For now needs manual download
		# try:
		# 	nltk.data.find('tokenizers/punkt.zip')
		# except LookupError:
		# 	nltk.download('punkt')
		
		# try:
		# 	nltk.data.find('maxent_treebank_pos_tagger')
		# except LookupError:
		# 	nltk.download('maxent_treebank_pos_tagger')
		
		self.id = text_id
		self.text = text
		self.tokens = []
		self.sentences = []
		self.tagged = []
		self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	
	def tokenize_sentences(self):
		self.sentences = nltk.sent_tokenize(self.text)
		
	def tokenize_words(self):
		if not self.sentences:
			self.tokenize_sentences()
		
		for sentence in self.sentences:
			# and here we also need to mark the position
			# span tokenize might be what I want
			print(self.tokenizer.span_tokenize(self.text))
			# self.tokens.extend(nltk.span_tokenize(self.text))
			
	def pos_tag(self):
		for sentence in self.tokens:
			self.tagged.append(nltk.pos_tag(sentence))
		
	# based on Osman's code	
	# TODO change this output directory to be within the text_processing directory
	def export_xml(self,output_directory='aq_nltk_tagged_files',mode='both'):
		import xml.etree.ElementTree as ET
		import os.path
		
		# create folder if it doesn't exist yet
		if not os.path.exists(output_directory):
			try:
				os.makedirs(output_directory)
			except():
				print('Could not create directory', output_directory)
				return None

		
		sentence_number = 0
		word_position = 0
		
		root = ET.Element("root")
		for sentence in self.tagged:
			S = ET.SubElement(root,"S")
			S.set('i',str(sentence_number))
			sentence_number = sentence_number + 1;
			
			for word in sentence:
				W = ET.SubElement(S,"W")
				W.text = word[0]
				W.set('pos',word[1])
				
				# find the starting position while skipping space characters
				while self.text[word_position:(word_position + len(word[0]))] != word[0]:
					word_position = word_position + 1
					if word_position > len(self.text):
						break
						
				# Create the o1 and o2 attributes for the starting and ending position of the word
				W.set('o1', str(word_position))
				word_position = word_position + len(word[0])
				W.set('o2', str(word_position))
		
		# write using etree
		file_name = os.path.join(output_directory, self.id + '.xml')
		if ( mode == 'both' or mode == 'normal' or mode == None ):
			with open(file_name,'wb') as f:
				ET.ElementTree(root).write(f,encoding="UTF-8",xml_declaration=True)
		
		# Pretty Print
		file_name = os.path.join(output_directory, self.id + '_pretty.xml')
		if ( mode == 'both' or mode == 'pretty' ) :
			from xml.dom import minidom
			
			pretty_article = minidom.parseString(ET.tostring(root, 'utf-8')).toprettyxml(indent="	")
			with open(file_name,'w') as f:
				f.write(pretty_article)