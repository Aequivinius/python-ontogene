#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Compares simhash and nilsimsa algorithms performance"""

# Use: python3 testing.py input_directory output_directory [ pickle file with entities ] percent_to_change

import os.path
import sys
import helpers
import random
import time
import csv

# PROCESS ARGUMENTS
input_directory = sys.argv[1]
output_directory = helpers.make_directory(sys.argv[2])
changed_files_directory = helpers.make_directory(os.path.join(output_directory,'mutations'))
simhash_directory = helpers.make_directory(os.path.join(output_directory,'simhashes'))
nilsimsa_directory = helpers.make_directory(os.path.join(output_directory,'nilsimsa'))



if len(sys.argv) >= 4:
	pickle_file = sys.argv[3]

percent_to_change = 50	
if len(sys.argv) >= 5:
	percent_to_change = sys.argv[4]

## Import 'seeding files'
original_files = list()

if os.path.exists(input_directory):
	
	# Will only use the first 100 to save processing time
	original_file_names = [ f for f in os.listdir(input_directory) if os.path.isfile(os.path.join(input_directory,f)) ][:100]
	original_files = [ os.path.join(input_directory,f) for f in original_file_names ]
else:
	print('No input_directory found. Make sure it exists.')
	
original_articles = list()
for original_file in original_files:
	with open(original_file,'r') as f:
		original_articles.append(f.read())

# GENERATING TEST FILES
## Create permutations of varying degrees
def generate_test_files():
	### In one case, just replace random characters and write
	start_characters = time.time()
	id_counter = 0
	for original_article in original_articles:
		# converting to list
		new_article = list(original_article)
		
		characters_to_change_number = int((len(original_article)*percent_to_change)/100)
		characters_to_change_positions = random.sample(range(len(original_article)),characters_to_change_number)
		characters_per_percent = int(characters_to_change_number/percent_to_change)
		
		print("Changing characters in article number " + str(id_counter))
	    
		for i in range(percent_to_change):
			for j in range(characters_per_percent):
			    # Latin-1 range
			    new_article[characters_to_change_positions[i*characters_per_percent+j]] = chr(32 + random.randint(0, 95))
			    
			file_name = os.path.splitext(os.path.basename(original_file_names[id_counter]))[0] + "_" + str(i) + "_percent_characters_changed.txt"
			with open(os.path.join(changed_files_directory,file_name),'w') as f:
	            # convert list to string
				f.write(''.join(new_article))
	        
		id_counter += 1
	            
	end_characters = time.time()
	print("Changed characters and wrote " + str(len(original_articles)) + " articles in " + str(end_characters - start_characters) + " seconds")
	
	### In the other case, replace tokens by other entities and write
	import nltk
	
	start_tokens = time.time()
	id_counter = 0
	terms = helpers.load_termlist_from_pickle(pickle_file)
	
	for original_article in original_articles:
		new_tokens = nltk.word_tokenize(original_article)
		
		tokens_to_change_number = int((len(new_tokens)*percent_to_change)/100)
		tokens_to_change_positions = random.sample(range(len(new_tokens)),tokens_to_change_number)
		tokens_per_percent = int(tokens_to_change_number/percent_to_change)
			
		random_tokens = [ ' '.join(f[1][0][0]) for f in random.sample(terms.items(),tokens_to_change_number) ]
		
		print("Changing tokens in article number " + str(id_counter))
		
		for i in range(percent_to_change):		
			for j in range(tokens_per_percent):
				new_tokens[tokens_to_change_positions[i*tokens_per_percent+j]] = random_tokens[i*tokens_per_percent+j]
				
			
			file_name = os.path.splitext(os.path.basename(original_file_names[id_counter]))[0] + "_" + str(i) + "_percent_tokens_changed.txt"
			with open(os.path.join(changed_files_directory,file_name),'w') as f:
			    f.write(' '.join(new_tokens))
	
		id_counter += 1
	
	end_tokens = time.time()
	print("Changed tokens and wrote " + str(len(original_articles)) + " articles in " + str(end_tokens - start_tokens) + " seconds")
	
# GENERATING CODES
mutated_file_names = [ f for f in os.listdir(changed_files_directory) if os.path.isfile(os.path.join(changed_files_directory,f)) ]
mutated_files = [ os.path.join(changed_files_directory,f) for f in mutated_file_names ]

mutated_articles = list()
for mutated_file in mutated_files:
	with open(mutated_file,'r') as f:
		mutated_articles.append(f.read())

## Starting with simhash
### Possibly want with different lengths
def simhashes():
	sys.path.append(os.path.join(os.path.dirname(__file__), 'hashes'))
	from hashes import simhash as s
	
	hashbit_lengths = [ 8 , 64 , 256 ]
	simhashes = dict()
	
	for hashbit_length in hashbit_lengths:
	    my_simhashes = dict()
	    start_simhash = time.time()
	    print("Processing " + str(len(mutated_articles)) + " mutated articles with Simhash and a hash length of " + str(hashbit_length))
	    
	    article_counter = 0
	    for article in mutated_articles:
	        my_simhashes[mutated_file_names[article_counter]] = s.simhash(article,hashbits=hashbit_length)
	        
	        article_counter += 1
	    
	    file_name = 'simhashes_' + str(hashbit_length) + "_bit.txt"
	    with open(os.path.join(simhash_directory,file_name),'w') as f:
	        writer = csv.writer(f,delimiter='\t')
	        for my_file_name , my_simhash in my_simhashes.items():
	            writer.writerow([my_file_name , my_simhash])
	            
	    simhashes[hashbit_length] = my_simhashes	
	    end_simhash = time.time()
	    print("Processed all files with Simhash and hash length of " + str(hashbit_length) + " in " + str(end_simhash - start_simhash) + " seconds")
		
## Nilsimsa
import nilsimsa as n

nilsimsas = dict()
article_counter = 0

start_nilsimsa = time.time()
print("Processing " + str(len(mutated_articles)) + " mutated articles with Nilsimsa")
for article in mutated_articles:
	nilsimsas[mutated_file_names[article_counter]] = n.Nilsimsa(article).hexdigest()
	
	article_counter += 1

with open(os.path.join(nilsimsa_directory,'nilsimsas.txt'),'w') as f:
	writer = csv.writer(f,delimiter='\t')
	for my_file_name , my_nilsimsa in nilsimsas.items():
		writer.writerow([my_file_name , my_nilsimsa])
		
end_nilsimsa = time.time()
print("Processed all files with Nilsimsa in " + str(end_nilsimsa - start_nilsimsa) + " seconds")


# COMPARING CODES
## Ideally, get a list of how much was changed
## and the distance between the generated codes