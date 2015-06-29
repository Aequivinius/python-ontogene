GENERAL PURPOSE
This project is a pipeline to extract relations between proteins in biomedical literature.

STRUCTURE
The pipeline has several stages, each of which is its own module. The pipeline is then run from control.py

1. import
2. 

TO DO
The pipeline is currently developed up to stage 4, that is, entity recognition. Besides the development of the following stages, the following things need doing:

* tidying up the code
* moving all the files and data to the module folders
* write export functions for every module
* document the code
	* check out sphinx
* get rid of the aq_ prefixes

* get word positions when tokenising, so I can use them in the ER
* keep note of entries like protein

* upload the project to some online repository, even if it’s my personal one
* test with big data

* do some more prolog
* start writing a report

* write export in Recognise entities
* write somewhere that it uses python3 , nltk with the punkt and mayent_treebank_pos_tagger


CHANGELOG

CREDITS
Nico Colic
ncolic@gmail.com
