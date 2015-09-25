#!/usr/bin/env python
# -*- coding: utf-8 -*-

# STAGE 0: Load configurations
from config import Configuration
my_config = Configuration()

# BOOKKEEPING
import time
start = time.time()
my_config.verbose_file.write("*************************\n")
my_config.verbose_file.write('started at ' + str(start)+ '\n')
		
# STAGE 1B: Importing from files
from text_import import file_import
articles = file_import.import_file('/Users/Qua/Downloads/data/1005')

# STAGE 2: low level text processing: tokenisation, PoS tagging
# How to use: first create an object Text_processing, which will have the tokenizer as a class variable. Use tokenizer.tokenize_words(text) to tokenize; use tokenizer.pos_tag(tokenized_words) to tag
from text_processing.text_processing import Text_processing as tp

my_tp = tp(word_tokenizer=my_config.word_tokenizer_object,
           sentence_tokenizer=my_config.sentence_tokenizer_object)

for article in articles:
	try:
		article.tokenize(tokenizer=my_tp)
	except:
		my_config.verbose_file.write('couldn\'t tokenize ' + str(article.id_) + '\n')
		
tokenized_time = time.time()
my_config.verbose_file.write('tokenized ' + str(len(articles)) + ' in ' + str(tokenized_time-start) + ' seconds\n')

# STAGE 3: entity recognition
# How to use: first create an object Entity_recognition, which takes as an argument a list of NEs to be found.
# Then use recognise_entities, giving the tokens of the text as a list, the funciton will return a list of found entities
from entity_recognition.entity_recognition import Entity_recognition as er

my_er = er(	my_config.termlist_file_absolute,
			my_config.termlist_format,
			word_tokenizer=my_tp,
			verbose=my_config.verbose,
			verbose_file=my_config.verbose_file )

counter = 0
start_er = time.time()
for article in articles:
	counter += 1
	try:
		article.recognize_entities(my_er)
		# article.print_entities_xml(my_config.output_directory_absolute + '/entities_' + str(article.id_) + '.xml', pretty_print=True)
	except:
		my_config.verbose_file.write('couldn\'t ER in ' + str(article.id_)+'\n')
		
	if (counter % 1000) == 0:
		now = time.time()
		my_config.verbose_file.write('ER in ' + str(counter) + ' articles in ' + str(start_er-now) +' seconds so far\n')

end = time.time()
my_config.verbose_file.write('*******************\n')
my_config.verbose_file.write('entire pipeline processed ' + str(len(articles)) + ' in ' + str(end-start) + ' seconds in total\n')
