#!/usr/bin/env python
# -*- coding: utf-8 -*-

from text_import.file_import import File_import
from text_import.pubmed_import import Pubmed_import
from text_processing.text_processing import Text_processing as tp
from entity_recognition.entity_recognition import Entity_recognition as er

# This is to ensure that both text_processing and entity_recognition use the same tokenizer
tokenizer = 'WordPunctTokenizer'

# STAGE 1: Importing, and converting
# Use either Pubmed_import or File_import, depending on what you need. Note that these objects will store handles for easy exporting of abstracts and texts, so create new object of respective class for every text instance.
# When using export_xml, the mode option allows to chose between normal xml and the slightly slower pretty xml

# my_pubmed = Pubmed_import('10516055',entrez_email='ncolic@gmail.com')
# my_pubmed.export_json()
# my_pubmed.export_xml(mode='both')

# # my_files = File_import('test_directory',load_complete_file='yes',text_key_xml='abstract')

my_file = File_import('test_directory/BEL-20000144.json')
# print(my_file.texts['BEL-20000144.json'])


# STAGE 2: low level text processing: tokenisation, PoS tagging
# How to use: first create an object Text_processing, which will have the tokenizer as a class variable. Use tokenizer.tokenize_words(text) to tokenize; use tokenizer.pos_tag(tokenized_words) to pos-tag
my_tp = tp(tokenizer=tokenizer)
tokens = my_tp.tokenize_words(my_file.texts['BEL-20000144.json'])
# print(tokens)
# pos_tagged = my_tp.pos_tag(tokens)
# print(pos_tagged)

# my_nltk = Aq_nltk(my_pubmed.get_abstract(),my_pubmed.pmid)
# my_nltk.tokenize_words()
# my_nltk.pos_tag()
# # my_nltk.export_xml()

# STAGE 3: entity recognition
# How to use: first create an object Entity_recognition, which takes as an argument a list of NEs to be found.
# Then use recognise_entities, giving the tokens of the text as a list, the funciton will return a list of found entities
# TODO: later on, you will be able to use Entiry_recognition's export functions to save these lists

my_er = er('entity_recognition/termlists/ontogene_terms_C_D_F03.tsv',termlist_format=6,tokenizer=tokenizer)
# entities = my_er.recognise_entities(words=tokens)
# print(entities)


