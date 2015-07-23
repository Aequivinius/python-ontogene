#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nico Colic, June 2015

import nltk
import os.path


class Text_processing(object):
	"""Allows to do tokenisation and PoS tagging on a given text"""
	"""For now, needs manual downloading in NLTK of tokenizers/punkt and maxent_treebank_pos_tagger before it works"""
	"""Structure of tokens: [0]: token, [1]: start position, [2]: end position"""
	"""Structure of tagged tokens: same as tokens, and [3] is tag"""
	
	sentence_tokenizer = None
	word_tokenizer = None
		
	def __init__(self, word_tokenizer, sentence_tokenizer):
		
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

		self.sentence_tokenizer = sentence_tokenizer
		self.word_tokenizer = word_tokenizer

	def tokenize_sentences(self, text):
		return self.sentence_tokenizer.tokenize(text)
	
	# to return two values doesn't make sense at all. so I'd rather have two functions, the first one returns tokens per sentences, and a flattify function	
	def tokenize_words(self, text):
		"""Returns a list of tokenizes sentences, which in turn are a list of token tuples. Use flatify() to get a flat list of tokens.
		Token tuples: [0] token text, [1] begin position, [2] end position, [3] sentence number"""
		sentences = self.tokenize_sentences(text)
		tokens_per_sentence = list()
		sentence_offset = 0
		
		sentence_counter = 0
		for sentence in sentences:
			sentence_tokens = list()
			for token in self.word_tokenizer.span_tokenize(sentence):
				# save actual token together with it's positions
				begin = token[0] + sentence_offset
				end = token[1] + sentence_offset
				token_tuple = (text[begin:end],begin,end,sentence_counter)
				sentence_tokens.append(token_tuple)
				
			tokens_per_sentence.append(sentence_tokens)
			
			sentence_counter = sentence_counter + 1
			sentence_offset = sentence_offset + len(sentence) + 1
		
		return tokens_per_sentence
	
	def flatify(self, tokens_per_sentence):
		tokens = list()
		
		for sentence in tokens_per_sentence:
			for token in sentence:
				tokens.append(token)
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
			
	def export_tokens_to_xml(self,id, tokens_per_sentence,output_directory,mode=None):
		import xml.etree.ElementTree as ET
		
		sentence_number = 0
		root = ET.Element("root")
		for sentence in tokens_per_sentence:
			S = ET.SubElement(root,"S")
			S.set('i',str(sentence_number))
			sentence_number = sentence_number + 1;
			
			for word in sentence:
				W = ET.SubElement(S,"W")
				W.text = word[0]
						
				# Create the o1 and o2 attributes for the starting and ending position of the word
				W.set('end', str(word[2]))
				W.set('begin', str(word[1]))
				
		
		# prepare printing
		my_directory = self.make_output_subdirectory(output_directory)
		
		# write using etree
		file_name = os.path.join(my_directory, id + '.xml')
		if ( mode == 'both' or mode == 'normal'):
			with open(file_name,'wb') as f:
				ET.ElementTree(root).write(f,encoding="UTF-8",xml_declaration=True)
		
		# Pretty Print
		file_name = os.path.join(my_directory, id + '_pretty.xml')
		if ( mode == 'both' or mode == 'pretty' or mode == None ) :
			from xml.dom import minidom
			
			pretty_article = minidom.parseString(ET.tostring(root, 'utf-8')).toprettyxml(indent="	")
			with open(file_name,'w') as f:
				f.write(pretty_article)
	
	def export_tagged_tokens_to_xml(self):
		pass
				
	def make_output_subdirectory(self,output_directory_absolute):
		my_directory = os.path.join(output_directory_absolute, 'text_processing')
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
