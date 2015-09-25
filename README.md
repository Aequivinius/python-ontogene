GENERAL PURPOSE
===============
The goal of this project is to set up a pipeline to extract relations between proteins in biomedical literature automatically. There is an existing pipeline, consisting of various modules in different programming languages; this project unifies them into one consistent pipeline written in python 3.

USAGE
=====
The pipeline is run using 'python3 main.py'. Make sure you consult config/config.py to change configuration of the pipeline.


STRUCTURE
=========
The pipeline has several stages, each of which is its own module. The pipeline is then run from main.py.

0. configuration
	All paths to various input or output directories, as well as pmids, for example, can be specified in the config/config.py
1. import
	This module allows downloading of articles from PubMed via Biopython, or to read them from a file. Returns an Article
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
	* don't spend too much time on file_import.py (but do it!)
	* a statistics function that appends to output/statistics_date_time.txt
		* might be best done in main.py

* text import
	* plain text export
	* check file_import
	* idea: have a script that automatically maintains up-to-date PubMed dump
	
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
		* BioC output
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

wieder null übersicht was geht. was wir wollen:
* die fucking pipeline fertig polieren
	* article
		* we left off at ER
		* bioc export
		* json export
		* unique ids throughout thing
		
	* import
		* add chemicals and meshes
	
	* tp
		* pos tagging
	
	* er
		* compare results to rinaldi
		* export
		
		
> jepp, in the end wollen wir ein kompaktes, gut dokumentiertes software package.
let's just start somewhere. ER

yeah, it makes sense to have this as a class.


do something about the tokenizer and config interaction. it shouldn't get an object from config, that's just dumb


write in documentation that we need a span_tokenize_words() function now. tokenize_words() is the plain one for the dictionary

okay, now I'm at the last step of finishing the er clean-up: make it work with the article class, and 
write exporters.

then I can setup the test, test and compare (do I still remember how to do that?), and put that in my paper. then volker.

then rewrite the rest and polish polish polish.


oki, so er works now well. now we need exporters from the article class, and then we can run it on the server and compare. I think the positions might be off, because I don't take into account the ofsets for the paragraphs.


the text variable of entity is not yet quite nice. it should be 1:1 what is in the text.

oh great, I can't test it on kitt for now.

so I run it on my compi, and then write report > send to rinaldini + proposal
then volker
then japan
then
in the meantime, polish more, and then run on kitt as soon as it's ready


oki, come on, prep the test



* rinaldi's paper fertig
* timing
* prolog
* python buch
* japan
* master
