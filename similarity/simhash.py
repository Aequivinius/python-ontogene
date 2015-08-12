#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Computes simhash values of various key lengths. Use as python3 simhash.py input_file_or_folder output_folder"""

import helpers
import sys
import os.path
from os import listdir
import time

from operator import itemgetter    

sys.path.append(os.path.join(os.path.dirname(__file__), 'hashes'))
from hashes import simhash as s
   
# IMPORTANT VARS
hashlengths = ( 8 , 64 )
files = list()
output_directory = sys.argv[2]

# PROCESSING OF ARGUMENTS: FILES
if os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1]) :
	files.append(os.path.abspath(sys.argv[1]))
	
if os.path.exists(sys.argv[1]) and os.path.isdir(sys.argv[1]):
	files = [ os.path.join(sys.argv[1],f) for f in listdir(sys.argv[1]) if os.path.isfile(os.path.join(sys.argv[1],f)) ]
	
if not os.path.exists(sys.argv[2]):
	print('Output folder doesn\'t exist, creating: ' + sys.argv[2])
	output_directory = helpers.make_directory(sys.argv[2])

print("Processing " + str(len(files)) + " files.")
start_time = time.time()		
for my_file in files:
	with open(my_file,'r') as f:
		my_text = f.read()
	
	with open(os.path.join(sys.argv[2],os.path.basename(my_file)),'w') as g:
		for hashlength in hashlengths:
			g.write(str(int(s.simhash(my_text,hashlength))) + '\n')
			
end_time = time.time()
print("Processed files in " + str(end_time - start_time))	

