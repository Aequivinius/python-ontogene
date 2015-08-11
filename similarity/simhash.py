#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import nilsimsa
import sys
import os.path
from os import listdir
import pickle
import time

from operator import itemgetter    
import random

sys.path.append(os.path.join(os.path.dirname(__file__), 'hashes'))
from hashes import simhash as s



"""Call as: python3 my_nilsimsa.py input_directory output_folder output-format
   Output format can be 'hex', can be 'decimal', 'both' or none (in which case it will output hex)"""
   
# IMPORTANT VARS
hashbits = 8

def make_directory(directory):
	"""Create folder if it doesn't exist yet"""
	if not os.path.exists(directory):
		try:
			os.makedirs(directory)
			return directory
		except():
			print('Could not create directory ', directory)
			return None
	else:
		return directory


# PROCESSING OF ARGUMENTS: FILES
if os.path.exists(sys.argv[1]):
	files = [ f for f in listdir(sys.argv[1]) if os.path.isfile(os.path.join(sys.argv[1],f)) ]

blocked_files = [ '.DS_Store' , 'nilsimsa_hex_values.pickle' , 'nilsimsa_hex_values.tsv' , 'nilsimsa_decimal_values.pickle' , 'nilsimsa_decimal_values.tsv' , 'simhash_hex_values.tsv' , 'simhash_hex_values.pickle' , 'simhash_decimal_values.tsv' , 'simhash_decimal_values.pickle']

for blocked_file in blocked_files:
	try:
		files.remove(blocked_file)
	except:
		pass

# PROCESSING OF ARGUMENTS: OUTPUT MODE
output_hex = False
output_decimal = False

try:
	if sys.argv[3] == 'hex' or sys.argv[3] == 'both':
		output_hex = True
		
	if sys.argv[3] == 'decimal' or sys.argv[3] == 'both':
		output_decimal = True
except:
	output_hex = True
	
# PROCESSING
hex_values = dict()
decimal_values = dict()
texts = dict()

start = time.time()
print("Commencing processing of " + str(len(files)) + " files.")

print(files)
for my_file in files: 
	
	my_hash = None
	with open(os.path.join(sys.argv[1],my_file),'r') as f:
		data = f.read()
		texts[my_file] = data
		my_hash = s.simhash(data,hashbits=hashbits)
	
	if output_hex:
		hex_values[my_file] = my_hash.hex()
	
	if output_decimal:
		decimal_values[my_file] = int(my_hash)

finish = time.time()
print("Finished processing files in " + str( finish - start ) + " seconds.")

# OUTPUTTING
output_directory = make_directory(sys.argv[2])
if output_hex:
	with open(os.path.join(output_directory,'simhash_hex_values.tsv'),'w') as f:
		f.write("FILE NAME\tNILSIMSA HEX VALUE\n")
		for key , value in hex_values.items(): 		
			f.write("%s\t%s\n" % (key,value))
			
	with open(os.path.join(output_directory,'simhash_hex_values.pickle'),'wb') as f:
		pickle.dump(hex_values,f)

if output_decimal:
	with open(os.path.join(output_directory,'simhash_decimal_values.tsv'),'w') as f:
		f.write("FILE NAME\tNILSIMSA DECIMAL VALUE\n")
		for key , value in decimal_values.items(): 		
			f.write("%s\t%s\n" % (key,value))
			
	with open(os.path.join(output_directory,'simhash_decimal_values.pickle'),'wb') as f:
		pickle.dump(decimal_values,f)

print("Written output files to " + output_directory)

# test_list = list()
# for key, value in decimal_values.items():
#     test_list.append(value)

sorted_decimals = list()
for key, value in sorted(decimal_values.items(), key=itemgetter(1)):
	sorted_decimals.append((key,value))

# BUCKET
for i in range(256):
	for j in range(len(sorted_decimals)):
		if sorted_decimals[j][1] == i:
			my_directory = make_directory(os.path.join(output_directory,str(i)))
			with open(os.path.join(my_directory,sorted_decimals[j][0]),'w') as f:
				f.write(texts[sorted_decimals[j][0]])

