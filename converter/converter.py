#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os.path
import csv
import helpers
import time

import xml.etree.ElementTree as ET
from xml.dom import minidom

elements = { 'article' : [ 'id' , 'pmid' , 'issn' , 'year' ] ,
             'article-title' : [ 'id' , 'type' ] , 
             'abstract' : [ 'id' , 'type' ] , 
             'chemicals' : [] ,
             'mesh' : [] , 
             'S' : [ 'id' , 'i' ] , 
             'W' : [ 'id' , 'o1' , 'o2' , 'C' , 'lemma' , 'stem' ] }


def process_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--debug", help="Debug mode: Prints information on standard output",
	                          action="store_true")
	parser.add_argument("input", help="Input file or folder containing input files")
	parser.add_argument("output", help="output_file or folder where output will be printed")
	
	arguments = parser.parse_args()
	
	# check if input exists, else try local directory, else fail
	if not os.path.exists(arguments.input):
		input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),arguments.input)
		if not os.path.exists(input_file):
			raise Exception('Input file not found')
	else: 
		input_file = arguments.input
	
	# check if file mode or directory mode
	file_mode = True	
	if os.path.isdir(input_file):
		file_mode = False
		
	if not file_mode:
		output_file = helpers.make_directory(arguments.output)
		files = [ os.path.join(input_file,f) for f in helpers.mylistdir(input_file) if os.path.isfile(os.path.join(input_file,f)) ]
	
	else:
		files = [ input_file ]
		output_file = arguments.output

	
	return file_mode , files , output_file , arguments.debug

def process_row(xml_object,row):
	for i in range(len(elements[row[0]]))[1:]:
		xml_object.set(elements[row[0]][i],row[i])

def parse_file_etree(input):
	
	article = None	
	elements_stack = list()
	with open(input, 'r') as f:
		reader = csv.reader(f, delimiter='\t')
		
		first_row = next(reader)
		if first_row[0] != 'article':
			raise TypeError('File has unexpected format')
		
		article = ET.Element('article')
		process_row(article,first_row)
		elements_stack.append(article)
		
		for row in reader:
			if row[0] in elements:
				element = ET.SubElement(elements_stack[-1],row[0])
				process_row(element,row)
				elements_stack.append(element)
				
			if row[0] == '-':
				elements_stack[-1].text = row[1]	
				
			if row[0] == '/':
				elements_stack.pop()
				
	return article

def pretty_print_xml(article,output_file):
	pretty_article = minidom.parseString(ET.tostring(article, 'utf-8')).toprettyxml(indent="	")
	with open(output_file,'w') as f:
		f.write(pretty_article)

def main():
	file_mode , files , output_file , debug = process_arguments()
	start = time.time()
	if file_mode:
		article = parse_file_etree(files[0])
		pretty_print_xml(article,output_file)
		
		end = time.time()
		
	else:
		for f in files:
			article = parse_file_etree(f)
			output_name = os.path.join(output_file, os.path.splitext(os.path.split(f)[1])[0] + ".xml")
			pretty_print_xml(article,output_name)
		end = time.time()
		
	if debug:
		print("Processed " + str(len(files)) + " in " + str(end - start) + " seconds")

if __name__ == "__main__":
	main()