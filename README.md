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
	* test with bigger data sets (use files in pmid folder)
		* find a way to deal with errorenous files
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
		* including a tsv format
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

so, until tomorrow the main thing is to get it nice and running for er, and have export for that. nice to have would be to figure out unicode, and config file.

then polish, and other export functions; and then we can deal with parsing.

okay, let's get started with ER

so this all seems to work well enough, so we really want
* find out ramanjini
* positions
* tsv export

let's get started! there's no ramanjini in the abstract; and somehow my ramanjini entries don't have a end number. where do they come from?

it exists as entity in the dictionary

it seems i fixed index blub, but why would it match the last '.' with the ramanjini strain...?

so we did that, now we can check the positions. that's a bit annoying, because I need to do it by hand to establish blubb,

also, we need to test it with many files! that's be interesting, but not for now, stick to positions and tsv export

okay, positions. komm her du textle


The rate of Helicobacter pylori resistance to antibiotics determines the cure rate of treatment regimens containing such antibiotics. To review the literature to determine the rates of H pylori resistance to metronidazole and clarithromycin in Canada, and whether these rates vary in different regions of Canada. The literature was reviewed extensively for the prevalence of antibiotic-resistant H pylori in Canada by searching MEDLINE from January 1980 to May 1999, as well as abstracts of the American Gastroenterology Association Digestive Disease Week, Canadian Digestive Disease Week and The European H pylori Study Group Meetings from January 1995 to May 1999. Eleven studies that estimated H pylori resistance to metronidazole resistance and nine that estimated resistance to clarithromycin in Canada were identified. Rates of resistance for metronidazole and clarithromycin varied from 11% to 48% and 0% to 12%, respectively. Studies that obtained their estimates using the E-test and those that did not clearly exclude patients who had undergone previous attempts at H pylori eradication had higher estimates of resistance, accounting for this variability in results. The prevalence of primary H pylori resistance in Canada appears to be 18% to 22% for metronidazole and less than 4% for clarithromycin. These rates appear to be consistent across the different regions studied in Canada, but many regions have not been studied.

how to best do this?

oh, just treat it as array and check in python...

nachtragen zeit

okay, so it's more or less constant, which would be the title I guess. but then the distance decreases, which would be the sentences. but it's not my positions, it must be theirs.

so, let's add the title and then check what's up with the sentences spaces / offsets.

so, we dealt with this. now is export time.


im a bit stuck with export function. what I want:
every module has export functions that can be called, that by default will write to output/their_folder/their_file

now, rather than to specify that for every module, it would be good to have a central variable that has this. that will be in the config file (similar to tokenizer). but then remove all the default options, it's a bit shit.

okay, so to every export function we give the path to the output folder, because maybe we want it to be somewhere else, but by default it will be in our folder (so we put that in the config file?)

but then my_er export will know to make a folder in the output folder.

my_er.export(to_export, folder)

then export will create folder in output directory, and write to it

every module will do that, so it's good to put that in a helper function. makedir(parent, child)

yeah, but now is the question of absolute vs relative paths. absolute paths are ugly, we want to avoid these; but if we want the user to have the option to export to outside of the main folder?

that's not so important, that's a nice to have feature. so for now, all is relative to control.py

yeah, hardcode the structure for now

sodele, now I can export in rinaldi's format. I send him an email asking for the meaning of the id

DID that, just need to ask him about importance of abstract and sentence. actually, not ask him, just do it. but it's not super important.

so, what's left to do now? I think I did the most important things so far, I'd like to tidy the stuff up now so I can give it a complete aus einem guss feel, especially with file access and default values every thing feels a bit patchworky.
