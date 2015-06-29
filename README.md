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

TO DO
=====
The pipeline is currently developed up to stage 3, that is, entity recognition. Besides the development of the following stages, the following things need doing:

* general
	* tidy up the code
	* rename modules (get rid of the silly aq_ prefix)
	* write xml and json export functions for all modules
	* write better documentation of the code (check out sphinx)
	* test with bigger data sets
	
* low level text processing
	* get word positions when tokenising so ER can use them

* entity recognition
	* find entries like 'protein'. Because the internal representation of the NEs to be found is a dictionary with the first word of the NE to be found as key; this leads to some entries having a huge list of potential NEs pointed to by a single first word. We can possibly find more efficient solutions to deal with this; possibly trees.
	
* project
	* do some more prolog
	* start to write a report

CREDITS
=======
Nico Colic
ncolic@gmail.com
