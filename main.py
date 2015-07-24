#!/usr/bin/env python
# -*- coding: utf-8 -*-

# STAGE 0: Load configurations
from config.config import Configuration
my_config = Configuration()

# STAGE 1A: Import texts from Pubmed
from text_import.file_import import File_import
from text_import.pubmed_import import Pubmed_import

pubmed_articles = dict()
for pmid in my_config.pmids:
	my_pubmed_article = Pubmed_import(pmid,my_config.pubmed_email)
	pubmed_articles[pmid] = my_pubmed_article
	print(my_pubmed_article.get_whole_abstract_minus_mesh(options=None, args=None))
	
	# my_pubmed_article.export_json(my_config.output_directory_absolute)
	# my_pubmed_article.export_xml(my_config.output_directory_absolute)
		
# STAGE 1B: Importing from files
# # my_files = File_import('test_directory',load_complete_file='yes',text_key_xml='abstract')

# STAGE 2: low level text processing: tokenisation, PoS tagging
# How to use: first create an object Text_processing, which will have the tokenizer as a class variable. Use tokenizer.tokenize_words(text) to tokenize; use tokenizer.pos_tag(tokenized_words) to tag
from text_processing.text_processing import Text_processing as tp

my_tp = tp(word_tokenizer=my_config.word_tokenizer_object,
           sentence_tokenizer=my_config.sentence_tokenizer_object)

tokens = dict()
for pmid, pubmed_article in pubmed_articles.items	():
    my_tokens = my_tp.tokenize_words(pubmed_article.get_whole_abstract_minus_mesh())
    tokens[pmid] = my_tokens
    my_tp.export_tokens_to_xml(pmid, my_tokens, my_config.output_directory_absolute)


# STAGE 3: entity recognition
# How to use: first create an object Entity_recognition, which takes as an argument a list of NEs to be found.
# Then use recognise_entities, giving the tokens of the text as a list, the funciton will return a list of found entities
# from entity_recognition.entity_recognition import Entity_recognition as er
# 
my_er = er(my_config.termlist_file_absolute,my_config.termlist_format,my_config.word_tokenizer_object)
entities = list()
for pmid, tokenized_text in tokens.items():
    my_entities = my_er.recognise_entities(sentences=tokenized_text)
    my_er.export_tsv_legacy_format(pmid, my_entities, my_config.output_directory_absolute)
    entities.extend(my_entities)


