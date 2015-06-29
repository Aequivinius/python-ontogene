#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aq_import.file_import import File_import
from aq_import.pubmed_import import Pubmed_import
from text_processing.text_processing import Text_processing as tp
from entity_recognition.entity_recognition import Entity_recognition as er

# This is to ensure that both text_processing and entity_recognition use the same tokenizer
tokenizer = 'WordPunctTokenizer'

my_file = File_import('test_directory/BEL-20000144.json')
print(my_file.texts['BEL-20000144.json'])


# # STAGE 1: Importing, and converting
# # my_files = File_import('test_directory',load_complete_file='yes',text_key_xml='abstract')
# my_pubmed = Pubmed_import('10516050',entrez_email='ncolic@gmail.com')
# # my_pubmed.export_json()
# # my_pubmed.export_xml()


# STAGE 2: low level text processing: tokenisation, PoS tagging
my_tp = tp(my_file.texts['BEL-20000144.json'],'BEL-20000144.json',tokenizer=tokenizer)
my_tp.tokenize_words()

# my_nltk = Aq_nltk(my_pubmed.get_abstract(),my_pubmed.pmid)
# my_nltk.tokenize_words()
# my_nltk.pos_tag()
# # my_nltk.export_xml()

# STAGE 3: entity recognition
# How to use: first create an object Entity_recognition, which takes as an argument a list of NEs to be found.
# Then use recognise_entities, giving the tokens of the text as a list, the funciton will return a list of found entities
# TODO: later on, you will be able to use Entiry_recognition's export functions to save these lists

my_er = er('entity_recognition/termlists/test_terms.csv',tokenizer=tokenizer, force_reload=1)
entities = my_er.recognise_entities(words=my_tp.tokens)
print(entities)


