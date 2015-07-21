#!/usr/bin/env python
# -*- coding: utf-8 -*-

from text_import.file_import import File_import
from text_import.pubmed_import import Pubmed_import
from text_processing.text_processing import Text_processing as tp
from entity_recognition.entity_recognition import Entity_recognition as er

# This is to ensure that both text_processing and entity_recognition use the same tokenizer
tokenizer = 'WordPunctTokenizer'

my_pmid = Pubmed_import('11111111', entrez_email='ncolic@gmail.com')
print(my_pmid.get_abstract())

my_tp = tp(tokenizer=tokenizer)
tokens = my_tp.tokenize_words(my_pmid.get_abstract())

my_er = er('entity_recognition/termlists/ontogene_terms_C_D_F03.tsv',termlist_format=6,tokenizer=tokenizer)
entities = my_er.recognise_entities(words=tokens)

for entity in entities:
	print(entity)