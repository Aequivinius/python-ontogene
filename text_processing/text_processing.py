#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nico Colic, June 2015

from nltk.tokenize import WordPunctTokenizer, PunktSentenceTokenizer
import nltk

class Text_processing(object):
	"""Allows to do tokenisation and PoS tagging on a given text"""
	"""For now, needs manual downloading in NLTK of tokenizers/punkt and maxent_treebank_pos_tagger before it works"""
	"""Structure of tokens: [0]: token, [1]: start position, [2]: end position"""
	"""Structure of tagged tokens: same as tokens, and [3] is tag"""
		
	def __init__(self, tokenizer='WordPunctTokenizer'):
		
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

		self.sentence_tokenizer = PunktSentenceTokenizer()
		self.word_tokenizer = None

		# Here you can add supported tokenizers. Note that it must implement the span_tokenize method
		if tokenizer == 'WordPunctTokenizer':
			self.word_tokenizer = WordPunctTokenizer()
				
		if tokenizer == 'PunktWordTokenizer':
			from nltk.tokenize import PunktWordTokenizer
			self.word_tokenizer = PunktWordTokenizer()
		
		if not self.word_tokenizer:
			print("Text processing: ", tokenizer, " you specified is not supported. Use default option or add in Text_processing.__init__(). Using default WordPunctTokenizer.")
			self.word_tokenizer = WordPunctTokenizer()
			
	def tokenize_sentences(self, text):
		return self.sentence_tokenizer.tokenize(text)
	
	# takes text as input	
	def tokenize_words(self, text):
		sentences = self.tokenize_sentences(text)
		tokens = list()
		sentence_offset = 0
		
		for sentence in sentences:
			for token in self.word_tokenizer.span_tokenize(sentence):
				# save actual token together with it's positions
				begin = token[0] + sentence_offset
				end = token[1] + sentence_offset
				tokens.append((text[begin:end],begin,end))
			
			sentence_offset = sentence_offset + len(sentence) + 1
		
		return tokens
	
	def pos_tag(self, span_tokens):
		"""Takes as input tokens with position information, and returns a list in the form of [0] token, [1] start position, [2] end position, [4] pos-tag"""
		
		# nltk.pos_tag() takes as argument a list of tokens, so we need to get rid of positions first, then pos-tag, then reconcile with position information
		tokens = list()
		
		for span_token in span_tokens:
			tokens.append(span_token[0])
		
		tagged_tokens = nltk.pos_tag(tokens)
		
		# reconcile with position information
		span_tagged_tokens = list()
		for i in range(len(span_tokens)):
			
			# just a little security measure should something go wrong
			if span_tokens[i][0] == tagged_tokens[i][0]:
				span_tagged_token = (span_tokens[i][0] , span_tokens[i][1] , span_tokens[i][2] , tagged_tokens[i][1])
				span_tagged_tokens.append(span_tagged_token)
		
		return span_tagged_tokens
			
	# based on Osman's code	
	# TODO change this output directory to be within the text_processing directory
	# TODO might be broken because tokens' format has changed
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