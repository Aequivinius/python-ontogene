GENERAL PURPOSE
===============
The goal of this project is to set up a pipeline to extract relations between proteins in biomedical literature automatically. There is an existing pipeline, consisting of various modules in different programming languages; this project unifies them into one consistent pipeline written in python 3.

USAGE
=====
The pipeline is run using 'python3 main.py'. Make sure you consult config.py to change configuration of the pipeline. Have a look at the example.py to see how the pipeline is run.


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
