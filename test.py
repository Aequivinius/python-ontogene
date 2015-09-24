#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nico Colic, September 2015

import article

# my_article = article.Article("123")
# 
# my_section = article.Section("s123","title","mine section is lamdamm")
# my_section.add_subelement(article.Token("token123","tokentext"))
# my_article.add_subelement(my_section)
# 
# print(my_article)

# from text_import.pubmed_import import pubmed_import
# 
# # article = Pubmed_import("12345678","ncolic@gmail.com") 
# article = pubmed_import("12346789","ncolic@gmail.com")
# article.print_xml('/Users/Qua/Downloads/asn.xml',pretty_print=1)

from text_import.file_import import import_file

articles = import_file('/Users/tabris/Downloads/data/test_data')


from config.config import Configuration
from text_processing.text_processing import Text_processing as tp

my_config = Configuration()

my_tp = tp(word_tokenizer=my_config.word_tokenizer_object,
sentence_tokenizer=my_config.sentence_tokenizer_object)

for my_article in articles:
	my_article.tokenize(tokenizer=my_tp)

from config.config import Configuration
my_config = Configuration()

from entity_recognition.entity_recognition import Entity_recognition as er

my_er = er(my_config.termlist_file_absolute,my_config.termlist_format,my_config.word_tokenizer_object)

for tokenized_article in articles:
	tokenized_article.recognize_entities()