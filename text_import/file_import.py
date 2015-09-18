#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nico Colic, September 2015

# Imports abstracts etc. from files in a directory, or from a single file
# Supports json, xml and txt

from os.path	import join, exists, isfile, split, isdir
from glob	import glob

import json
import xml.etree.ElementTree as ET

from article import Article

"""Loads texts from files in TXT. XML and JSON still need implementing."""

def import_file(path):
	"""Entry function, which can always be used. Will check if path is file or directory, and call respective functions"""
	"""Returns a list of Article objects"""	
	
	if isfile(path) :
		if path[-5:] == '.json' or path[-4:] == '.xml' or path[-4:] == '.txt' :
			return [ file_import(path) ]
	
	elif isdir(path) :
		return directory_import(path)
		
	else:
		print('File or directory does not exist') 
	
def directory_import(path):
	
	# add supported files in directory
	files = list()
	files.extend(glob(join(path,'*.json')))
	files.extend(glob(join(path,'*.xml')))
	files.extend(glob(join(path,'*.txt')))
	
	# try or something
	if len(files) == 0:
		print('No matching files found. Supported formats are XML, JSON, TXT')
		return None
	
	articles = list()
	
	for file_ in files:
		articles.append(file_import(file_))
		
	return articles

def file_import(path):
	"""Returns an Article object. Will set Article id_ to file_name"""
	
	file_name = split(path)[-1]
	with open(path) as f:
		if file_name[-5:] == '.json':
			article = json_to_article(f,file_name)
			
		if file_name[-4:] == '.xml':
			article = xml_to_article(f,file_name)
			
		if file_name[-4:] == '.txt':
			article = txt_to_article(f,file_name)
			
	return article

def json_to_article(file_,file_name):
	"""Not yet implemented"""
	pass
	
def xml_to_article(file_,file_name):
	"""Not yet implemented"""

	
def txt_to_article(file_,file_name):
	text = file_.read().strip('\n')
	article = Article(file_name.split('.')[0])
	article.add_section('', text)
	return article
