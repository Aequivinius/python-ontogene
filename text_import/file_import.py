#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nico Colic

# Imports abstracts etc. from files in a directory, or from a single file
# Supports json, xml and txt
# By default, it will only extract and keep in memory texts, not entire files, for better performance.

from os.path	import join, exists, isfile, split
from glob	import glob

from xml.etree import ElementTree as ET

import json

class File_import(object):
	
	def __init__(self, path, text_key_json='text', text_key_xml='text', load_complete_file=None):
		self.path = path
		self.text_key_json = text_key_json
		self.text_key_xml = text_key_xml
		
		self.files = []
		self.jsons = {}
		self.xmls  = {}
		self.texts = {}
		
		if not exists(path) :
			raise IOError('File or directory does not exist')
		
		if isfile(path) :
			if path[-5:] == '.json' or path[-4:] == '.xml' or path[-4:] == '.txt' :
				self.files.append(path)
		
		else :
			# add all supported files in directory
			self.files.extend(glob(join(path,'*.json')))
			self.files.extend(glob(join(path,'*.xml')))
			self.files.extend(glob(join(path,'*.txt')))
						
		if not self.files :
			raise IOError('No matching files found. Supported formats are XML, JSON, TXT')
				
		for my_file in self.files :
			my_file_name = split(my_file)[-1]
			
			with open ( my_file ) as my_opened_file :
				
				if my_file_name[-5:] == '.json':
					self.extract_json(my_opened_file,my_file_name,text_key_json,load_complete_file)
					
				if my_file_name[-4:] == '.xml':
					self.extract_xml(my_opened_file,my_file_name,text_key_xml,load_complete_file)
					
				if my_file_name[-4:] == '.txt':
					self.extract_txt(my_opened_file,my_file_name)
									
	def extract_json(self,my_file,my_file_name,key,load_complete_file):
		my_json = json.load ( my_file )
		self.texts[my_file_name] = my_json[key]
		
		if load_complete_file:
			self.jsons[my_file_name] = my_json
	
	def extract_xml(self,file,my_file_name,key,load_complete_file):
		my_xml = ET.parse(my_file_name)
		my_root = my_xml.getroot()
		my_text = my_root.find(key).text
		self.texts[my_file_name] = my_text
		
		if load_complete_file:
			self.xmls[my_file_name] = my_xml
		
	def extract_txt(self,file,my_file_name):
		my_text = file.read().strip('\n')
		self.texts[my_file_name] = my_text