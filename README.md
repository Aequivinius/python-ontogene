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


here we are again. if I don't want to fuck it up completely, I need to get some real work done, and it's gotta happen now and on monday (where I have work... fuck)

* finish article class and rewrite modules to be all sleek an clean
* include the changes fabio requested

* then we have the rest, like report (but fabio focuses on that!), prolog, python, japan

we're still at this stage where we want tokenization to be in the article class
in a way that it can be run from console...?

Pubmed import is a factory, so to say, returns article object


okay I spend too much time thinking about this, fabio said to put tokenization into article.

to it will be

article = import_module.import(pmid)
article.tokenize(give tokenizer from config)

and the rest



alrighty, back to it. somehow, it doesn't get the article object in the main.py
so the issue must lie in pubmed import to not return something?
 that was easier than expected.
 oki, we want tokenisation in the article class.



Okay, now there was a long time of not doing shit, and I need to figure it out now. 




alrighty, let's get started. the article class doesn't seem toooooo hard, really


argh, when rewriting I want to make them fit for being used by the command line, too. but for now just finish the article class and making the existing modules compatible with it (as far as possible, still want to cello etc.)

but now comes the interesting bit -> convert the record into article





for laters:
* make them fit for commandline
* do pubmed import as a factory, so I only have to deal with dump dir once
* make clear names for what is being pickled in pubmed_download: it's not .article, it's a entrez / biopython format shit. -> add extensions
* in the conversion biopython to article, we can keep all the meta-data?




* as for the code, I need to write this article class, and change my modules to work with it. And ideally polish them all, add BioC etc
	* and also, I should surprise him with a parser, so tomorrow I can ask him to do the other modules and we're good to go


* there's the report, which I just need to update with rinaldinis comments. that's no biggie. I should also document my doing of tonight

* and then there is the rest: prolog, sphinx, python book
* and japan, ofc, for which I should look at the forms.
