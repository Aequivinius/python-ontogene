#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nilsimsa
import sys
import os.path
from os import listdir
import pickle
import time

"""Call as: python3 my_nilsimsa.py input_directory output_folder output-format
   Output format can be 'hex', can be 'decimal', 'both' or none (in which case it will output hex)"""

def find_similar(needle,haystack):
	similars = list()
	for key , value in haystack.items():
		score = nilsimsa.compare_digests(needle, value, is_hex_1=False, is_hex_2=False, threshold=24 ) 
		if score > 24:
			similars.append(key)
	return similars
	
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

blocked_files = [ '.DS_Store' , 'nilsimsa_hex_values.pickle' , 'nilsimsa_hex_values.tsv' , 'nilsimsa_decimal_values.pickle' , 'nilsimsa_decimal_values.tsv' ]

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

start = time.time()
print("Commencing processing of " + str(len(files)) + " files.")

for my_file in files: 
	
	my_nilsimsa = nilsimsa.Nilsimsa()
	my_nilsimsa.from_file(os.path.join(sys.argv[1],my_file))

	if output_hex:
		hex_values[my_file] = my_nilsimsa.hexdigest()
	
	if output_decimal:
		decimal_values[my_file] = my_nilsimsa.digest()

finish = time.time()
print("Finished processing files in " + str( finish - start ) + " seconds.")

# OUTPUTTING
output_directory = make_directory(sys.argv[2])
if output_hex:
	with open(os.path.join(output_directory,'nilsimsa_hex_values.tsv'),'w') as f:
		f.write("FILE NAME\tNILSIMSA HEX VALUE\n")
		for key , value in hex_values.items(): 		
			f.write("%s\t%s\n" % (key,value))
			
	with open(os.path.join(output_directory,'nilsimsa_hex_values.pickle'),'wb') as f:
		pickle.dump(hex_values,f)

if output_decimal:
	with open(os.path.join(output_directory,'nilsimsa_decimal_values.tsv'),'w') as f:
		f.write("FILE NAME\tNILSIMSA DECIMAL VALUE\n")
		for key , value in decimal_values.items(): 		
			f.write("%s\t%s\n" % (key,value))
			
	with open(os.path.join(output_directory,'nilsimsa_decimal_values.pickle'),'wb') as f:
		pickle.dump(decimal_values,f)

print("Written output files to " + output_directory)

		
# find_similar(my_nilsimsas['11334364.txt'], my_nilsimsas)
	
# To compare two hex values, use the following function. digest_1 and _2 will be the hex values, threshold can be set to a value between -128 and 128, which will abort comparison if difference of the two digests is below it, thus speeding up comparison

# nilsimsa.compare_digests(digest_1, digest_2, is_hex_1=True, is_hex_2=True, threshold=None)
