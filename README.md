GENERAL PURPOSE
===============
The goal of this project is to set up a pipeline to extract relations between proteins in biomedical literature automatically. There is an existing pipeline, consisting of various modules in different programming languages; this project unifies them into one consistent pipeline written in python 3.

USAGE
=====
The pipeline is run using 'python3 control.py'


STRUCTURE
=========
The pipeline has several stages, each of which is its own module. The pipeline is then run from control.py

1. import
	This module allows downloading of articles from PubMed via Biopython, or to read them from a file
2. low level text processing
	This module uses NLTK for tokenisation and PoS tagging of the text.
3. entity recognition
	This module uses a supplied list of named entities and returns their positions in the text

CHANGES
=======
* low level text processing
	* this class used to store the text and the tokens as a class variable. Now, however, this falls into the responsibility of control.py. The tp class will only store the tokenizer, and return tokenized text from the tokenize_words() function.


TO DO
=====
The pipeline is currently developed up to stage 3, that is, entity recognition. Besides the development of the following stages, the following things need doing:

* general
	* test with bigger data sets (use files in pmids folder)
		* find a way to deal with erronous files
	* might be a good idea to write a sample control with hypothetical string to show how to use the pipeline
	* configuration file
		* go through code and tidy up, get rid of default values, maybe write a helper file
	
* text import
	* test import from file
	* tidy up unicode() problem from yesterday
	* export function
	* also look at title!
	
* text processing
	* export function
		* change folder to output/text_processing
	
* entity recognition
	* export function
		* add sentence number and origin within document (abstract, title) to tsv
	* check positions
	* make sure dictionary is loaded correctly, there seems to be too little entries
	* find entries like 'protein'. Because the internal representation of the NEs to be found is a dictionary with the first word of the NE to be found as key; this leads to some entries having a huge list of potential NEs pointed to by a single first word. We can possibly find more efficient solutions to deal with this; possibly trees.
	
* parsing
	* read up on stanford parser
		* interface it
	* check malt parser
	* other parsers?
	
* project
	* do some more prolog
	* start to write a report
	* check out shpinx
	* read a python best practises book

CREDITS
=======
Nico Colic
ncolic@gmail.com

STREAM OF CONSCIOUSNESS
=======================

