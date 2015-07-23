#!/usr/bin/env python
# -*- coding: utf-8 -*-


from entity_recognition.entity_recognition import Entity_recognition as er

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
	
	my_pubmed_article.export_json(my_config.output_directory_absolute)
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
	my_tp.export_tokens_to_xml(my_tokens, my_config.output_directory_absolute, mode=None)
	tokens[pmid] = my_tokens

	
	
		
# tokens = my_tp.tokenize_words(my_file.texts['BEL-20000144.json'])
# print(tokens)
# pos_tagged = my_tp.pos_tag(tokens)
# print(pos_tagged)

# tokenized_text = dict()
# my_tp = tp(tokenizer=config.tokenizer)
# for pmid , downloaded_pmid in downloaded_pmids.items():
#     try:
#         print(downloaded_pmid.get_abstract())
#     except:
#         i=0

# STAGE 3: entity recognition
# How to use: first create an object Entity_recognition, which takes as an argument a list of NEs to be found.
# Then use recognise_entities, giving the tokens of the text as a list, the funciton will return a list of found entities
# TODO: later on, you will be able to use Entiry_recognition's export functions to save these lists

# my_er = er('entity_recognition/termlists/ontogene_terms_C_D_F03.tsv',termlist_format=6,tokenizer=config.tokenizer)
# entities = my_er.recognise_entities(words=tokens)
# print(entities)


