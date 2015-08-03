GENERAL PURPOSE
===============
The goal of this project is to set up a pipeline to extract relations between proteins in biomedical literature automatically. There is an existing pipeline, consisting of various modules in different programming languages; this project unifies them into one consistent pipeline written in python 3.

USAGE
=====
The pipeline is run using 'python3 main.py'. Make sure you consult config/config.py to change configuration of the pipeline.


STRUCTURE
=========
The pipeline has several stages, each of which is its own module. The pipeline is then run from main.py.

1. import
	This module allows downloading of articles from PubMed via Biopython, or to read them from a file
2. low level text processing
	This module uses NLTK for tokenisation and PoS tagging of the text.
3. entity recognition
	This module uses a supplied list of named entities and returns their positions in the text
4. parsing
	This module will be developed.

CHANGES
=======
* VII
	* added config file
* VI: low level text processing
	* this class used to store the text and the tokens as a class variable. Now, however, this falls into the responsibility of main.py. The tp class will only store the tokenizer, and return tokenized text from the tokenize_words() function.


TO DO
=====
The pipeline is currently developed up to stage 3, that is, entity recognition. Besides the development of the following stages, the following things need doing:

* general
	* compare to the tsv output of Fabio's pipeline
	* don't spend too much time on file_import.py
	* a statistics function that appends to output/statistics_date_time.txt
		* might be best done in main.py
	* add plain text export

* text import
	* plain text export
	* check file_import
	
* text processing
	* add export functions (json, plain text)
	* add xml, json, plain text for pos-tagged, too
	* tsv?
	* also change structure of tagged words to reflect sentence structure
	
* Nilsimsa
	* integrate in pipeline
	* read up if there's a good way to sort / buckets
	* other algorithms
	
* entity recognition
	* export function
		* add sentence number and origin within document (abstract, title) to tsv (like in the script on kitt)
	* make sure dictionary is loaded correctly, there seem to be too few entries
	
* parsing
	* read up on stanford parser
		* interface it
	* check malt parser
	* other parsers?
	
* complex questions
	* paralellisation
	* find entries like 'protein'. Because the internal representation of the NEs to be found is a dictionary with the first word of the NE to be found as key; this leads to some entries having a huge list of potential NEs pointed to by a single first word. We can possibly find more efficient solutions to deal with this; possibly trees.

* report
	* set up latex
	* install latex diff
	
* project
	* check out shpinx
	* read a python best practises book
	* do some more prolog


CREDITS
=======
Nico Colic
ncolic@gmail.com

STREAM OF CONSCIOUSNESS
=======================