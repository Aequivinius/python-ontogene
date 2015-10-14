#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

# STAGE 0: Load configurations
# In the config.py file, you can change important variables such as tokenizer to use
import config
my_config = config.Configuration()

# for easier testing, you could supply a list of PMIDs in the constructor here
# my_config = config.Configuration([ 10193204 , 12345678 ])

# STAGE 1A: Import texts from Pubmed
from text_import.pubmed_import import pubmed_import

pubmed_articles = dict()
for pmid in my_config.pmids:
	my_pubmed_article = pubmed_import(pmid,my_config.pubmed_email)
	pubmed_articles[pmid] = my_pubmed_article
	my_pubmed_article.print_xml(os.path.join(my_config.output_directory_absolute,pmid + ".xml"))

# STAGE 1B: Importing from files
from text_import.file_import import import_file

try:
	file_articles = import_file('/absolute/path/to/directory/or/file')
except:
	print("No file or directory found")

# STAGE 2: low level text processing: tokenisation, PoS tagging
# How to use: first create an object Text_processing, which will have the tokenizer as a class variable. Use tokenizer.tokenize_words(text) to tokenize; use tokenizer.pos_tag(tokenized_words) to tag

from text_processing.text_processing import Text_processing as tp

my_tp = tp(word_tokenizer=my_config.word_tokenizer_object,
		   sentence_tokenizer=my_config.sentence_tokenizer_object)

for pmid, pubmed_article in pubmed_articles.items	():
	pubmed_article.tokenize(tokenizer=my_tp)
	my_pubmed_article.print_xml(os.path.join(my_config.output_directory_absolute,pmid + ".tokenized.xml"))

# STAGE 3: entity recognition
# How to use: first create an object Entity_recognition, which takes as an argument a list of NEs to be found.
# Then use recognise_entities, giving the tokens of the text as a list, the funciton will return a list of found entities
from entity_recognition.entity_recognition import Entity_recognition as er

my_er = er(	my_config.termlist_file_absolute,
			my_config.termlist_format,
			word_tokenizer=my_tp,
			verbose = my_config.verbose,
			verbose_file = my_config.verbose_file )

for pmid, tokenized_article in pubmed_articles.items():
	tokenized_article.recognize_entities(my_er)
	tokenized_article.print_entities_xml(my_config.output_directory_absolute + '/entities/' + str(pmid) + '.xml')