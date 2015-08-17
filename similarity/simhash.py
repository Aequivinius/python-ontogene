#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Computes simhash values of various key lengths. 
Use as python3 simhash.py input_folder output_folder
Or use as python3 simhash.py input_file output_file
You can also supply hashlengths as subsequent arguments, in which case the hashlengths variable will be overwritten. In this case, use as
python3 simhash.py input output 8 128 444 666 127 ..."""

import helpers
import sys
import os.path
from os import listdir
import time

sys.path.append(os.path.join(os.path.dirname(__file__), 'hashes'))
from hashes import simhash as s
   
def main():
	# IMPORTANT VARS
	# hashlengths = [ 8 , 64 ]
	hashlengths = [8, 16, 24, 32, 40, 48, 56, 64]
	
	# ARGUMENTS PROCESSING
	files = list()
	file_mode = False # used when processing just a single file instead of folder
	
	if os.path.exists(sys.argv[1]):
		if os.path.isfile(sys.argv[1]) :
			files.append(os.path.abspath(sys.argv[1]))
			file_mode = True
	
		elif os.path.isdir(sys.argv[1]):
			files = [ os.path.join(sys.argv[1],f) for f in listdir(sys.argv[1]) if os.path.isfile(os.path.join(sys.argv[1],f)) ]
		
	if not file_mode and not os.path.exists(sys.argv[2]):
		print('Output folder doesn\'t exist, creating: ' + sys.argv[2])
		output_directory = helpers.make_directory(sys.argv[2])
		
	if len(sys.argv) > 3:
		hashlengths = [ ]
		i = 3
		while i < len(sys.argv):
			hashlengths.append(int(sys.argv[i]))
			i += 1
		hashlengths.sort()
		
	print(hashlengths)

	# COMMENCE THE PROCESSING
	print("Processing " + str(len(files)) + " files.")
	start_time = time.time()
	
	if file_mode: # placed outside of loop to speed up processing of big directories
		with open(files[0],'r') as f:
			my_text = f.read()
		
		with open(sys.argv[2],'w') as g:
			for hashlength in hashlengths:
				write_hex_key(g,my_text,hashlength)
		end_time = time.time()
	
	else:
		for my_file in files:
			with open(my_file,'r') as f:
				my_text = f.read()
			
			with open(os.path.join(sys.argv[2],os.path.basename(my_file)),'w') as g:
				for hashlength in hashlengths:
					my_simhash = s.simhash(my_text,hashlength)
					write_hex_key(g,my_simhash,hashlength)
		end_time = time.time()
	
	print("Processed " + str(len(files)) + "files in " + str(end_time - start_time))	

def write_decimal_key(file_handle,simhash):
	file_handle.write(str(int(simhash))  + '\n')

def write_hex_key(file_handle,simhash,length):
	form="%%0%dX\n" % (length // 4)
	out=form % int(simhash)
	file_handle.write(out[::-1])
	


if __name__ == "__main__":
	main()
