#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nico Colic, July 2015
# Based on code by Tilia Ellendorff

import pickle # Python 3 will automatically try to use cPickle
from Bio import Entrez
import os
import time

# A file loaded as pickle from a PubMed dump in Biopython format
class Pubmed_import(object):
	"""Downloads file from Pubmed if it has not been downloaded before, otherwise returns previously downloaded version"""

	def __init__(self, pmid, dump_dir=None, entrez_email=None, options=None, args=None):
		"""If you want to supply other directory for storing and looking for previously downloaded files, supply absolute path"""
		self.pmid = pmid
		
		if dump_dir == None:
			my_directory = os.path.dirname(os.path.abspath(__file__))
			self.dump_dir = os.path.join(my_directory, 'dumps')
			self.path = os.path.join(self.dump_dir,pmid)
			
		else:
			self.path = os.path.join(dump_dir,pmid)

		# create folder if it doesn't exist yet
		if not os.path.exists(os.path.dirname(self.path)):
			try:
				os.makedirs(os.path.dirname(self.path))
			except():
				print('Could not create directory', self.dump_dir)
				return None

		if not self.pmid in os.listdir(self.dump_dir):
			print('ATTEMPT TO DOWNLOAD DATA FOR', self.pmid)
			self.download_pmid_data(entrez_email, options=options, args=args)
			time.sleep(1) # to prevent too many downloads to pmid, which will get you blocked
			print('DOWNLOADED AND WRITTEN TO FILE')

		try:
			self.file = open(self.path, 'rb')
			self.text = pickle.load(self.file)

		except (IOError, EOFError, AttributeError):
			print('ERROR, NO DATA FOR', self.pmid)
			return None

	def download_pmid_data(self, entrez_email, options=None, args=None):

		if entrez_email == None:
			print('DOWNLOAD OF NEW DATA CANNOT BE COMPLETED, PLEASE GIVE YOUR EMAIL.')
			return None

		Entrez.email = entrez_email
		print('THE DATA FOR PUBMED-ID', self.pmid, 'WILL BE DOWNLOADED')

		handle = Entrez.efetch(db="pubmed", id=self.pmid, retmode="xml")
		record = Entrez.read(handle)
		
		with open(self.path, 'wb') as f:
			
			# TODO: find out why it only works when I use protocol=1
			pickle.dump(record,f,protocol=1)

	def get_data(self, options=None, args=None):
		try:
			return self.text[0]
		except (IndexError, KeyError):
			print(self.pmid, 'no text_dict found', self.text)

	def get_abstract(self, options=None, args=None):
		try:
			text_dict = self.text[0]
			abstract = text_dict[u'MedlineCitation'][u'Article'][u'Abstract'][u'AbstractText']
			if len(abstract) == 1:
				return ' '.join(abstract)

			else:
				abstract_list = [str(abstract[i]) for i in range(len(abstract))] # was unicode
				abstract_string = ' '.join(abstract_list)
				return abstract_string

		except (IndexError, KeyError, AttributeError):
			return None

	def get_title(self, options=None, args=None):
		try:
			text_dict = self.text[0]
			return str(text_dict[u'MedlineCitation'][u'Article'][u'ArticleTitle'])
			# was unicode(...)

		except (IndexError, KeyError, AttributeError):
			return None

	def get_mesh(self, options=None, args=None):
		try:
			text_dict = self.text[0]
			mesh_list = text_dict[u'MedlineCitation'][u'MeshHeadingList']
			descriptor_list = [unicode(mesh_list[i][u'DescriptorName']) for i in range(len(mesh_list))]
			#print descriptor_list
			descriptor_dict = dict((n, descriptor_list[n]) for n in range(len(descriptor_list)))
			#for k, v in sorted(descriptor_dict.items()):
			#    print k,v
			qualifier_list = dict((i, [unicode(item) for item in mesh_list[i][u'QualifierName']]) for i in range(len(mesh_list)))
			#print self.pmid
			#for number, qualifier in qualifier_list.items():
			#    print number,  qualifier
		except (IndexError, KeyError):
			return None

	def get_mesh_descriptors(self, options=None, args=None):
		try:
			text_dict = self.text[0]
			mesh_list = text_dict[u'MedlineCitation'][u'MeshHeadingList']
			descriptor_list = [str(mesh_list[i][u'DescriptorName']) for i in range(len(mesh_list))]
			return '; '.join(descriptor_list)
			# was unicode(
		except (IndexError, KeyError):
			return None


	def get_mesh_qualifiers(self, options=None, args=None):
		try:
			text_dict = self.text[0]
			mesh_list = text_dict[u'MedlineCitation'][u'MeshHeadingList']
			#qualifier_list = list(set(sum([one_value for one_value in dict((i, [unicode(item) for item in mesh_list[i][u'QualifierName']]) for i in range(len(mesh_list))).values()], [])))
			qualifier_list = list(set(sum([[unicode(item) for item in mesh_list[i][u'QualifierName']] for i in range(len(mesh_list))], [])))
			return '; '.join(qualifier_list)
		except (IndexError, KeyError):
			return None


	def get_whole_abstract(self, options=None, args=None):
		try:
			whole_abstract_list = []
			whole_abstract_list.append(self.pmid + '. ')
			whole_abstract_list.append(self.get_title())
			whole_abstract_list.append(self.get_abstract())

			if not self.get_mesh_descriptors() == None:
				whole_abstract_list.append(self.get_mesh_descriptors())

			return ' '.join(whole_abstract_list)

		except (IndexError, KeyError, TypeError):
			return None

	def get_abstract_minus_mesh(self, options=None, args=None):
		try:
			whole_abstract_list = []
			whole_abstract_list.append(self.pmid + '. ')
			whole_abstract_list.append(self.get_title())
			whole_abstract_list.append(self.get_abstract())

			return ' '.join(whole_abstract_list)

		except (IndexError, KeyError, TypeError):
			return None
	
	def export_xml(self,output_directory='converted_files',mode=None):
		import xml.etree.ElementTree as ET
		pmid_medline = self.text[0][u'MedlineCitation']
		
		# BUILDING THE TREE
		article = ET.Element('article')
		article_attributes = {	'id':'',
							 	'issn':pmid_medline[u'Article'][u'Journal'][u'ISSN'],
								# 'pid':X,
								# 'pmcid':X,
							 	'pmid':pmid_medline[u'PMID'],
							 	'type':pmid_medline[u'Article'][u'PublicationTypeList'][0],
							 	'year':pmid_medline[u'DateCompleted'][u'Year']
								};
		for attribute, value in article_attributes.items():
			article.set(attribute,value)
		
		article_title = ET.SubElement(article,'article_title')
		article_title.set('id','')
		article_title.set('type','Title')
		article_title.text = pmid_medline[u'Article'][u'ArticleTitle']
		
		abstract = ET.SubElement(article,'abstract')
		abstract.set('id','')
		abstract.set('type','')
		abstract.text = pmid_medline[u'Article'][u'Abstract'][u'AbstractText'][0]
		
		chemicals = ET.SubElement(article,'chemicals')
		chemicals.set('id','')
		for chemical in pmid_medline[u'ChemicalList']:
			c = ET.SubElement(chemicals, 'chemical')
			c.set('UI',chemical[u'NameOfSubstance'].attributes[u'UI'])
			c.set('RegistryNumber',chemical[u'RegistryNumber'])
			c.text = chemical[u'NameOfSubstance']
		
		mesh = ET.SubElement(article,'mesh')
		mesh.set('id','')
		for mesh_element in pmid_medline[u'MeshHeadingList']:
			m = ET.SubElement(mesh, 'm')
			m.text = mesh_element[u'DescriptorName']
			m.set('UI',mesh_element[u'DescriptorName'].attributes[u'UI'])
			major_topic = mesh_element[u'DescriptorName'].attributes[u'MajorTopicYN']
			m.set('MajorTopicYN',major_topic)
		
			qualifier_name = mesh_element[u'QualifierName']
			if qualifier_name != []:
				m.set('qualifier_name',qualifier_name[0])
				m.set('qualifier_name_UI',qualifier_name[0].attributes[u'UI'])
				qualifier_name_major_topic = qualifier_name[0].attributes[u'MajorTopicYN']
				if major_topic != qualifier_name_major_topic:
					m.set('qualifier_name_major_topic',qualifier_name_major_topic)
		
		my_directory = os.path.dirname(os.path.abspath(__file__))
		absolute_output_directory = os.path.join(my_directory,output_directory)
		
		# create folder
		if not os.path.exists(absolute_output_directory):
			try:
				os.makedirs(absolute_output_directory)
			except():
				print('Could not create directory', absolute_output_directory)
				return None
		
		# write using etree
		file_name = os.path.join(absolute_output_directory, self.pmid + '.xml')
		if ( mode == 'both' or mode == 'normal' or mode == None ):
			with open(file_name,'wb') as f:
				ET.ElementTree(article).write(f,encoding="UTF-8",xml_declaration=True)
		
		# Pretty Print
		file_name = os.path.join(absolute_output_directory, self.pmid + '_pretty.xml')
		if ( mode == 'both' or mode == 'pretty' ) :
			from xml.dom import minidom
			
			pretty_article = minidom.parseString(ET.tostring(article, 'utf-8')).toprettyxml(indent="	")
			with open(file_name,'w') as f:
				f.write(pretty_article)
	
	def export_json(self,output_directory='converted_files'):
		import json
		
		my_directory = os.path.dirname(os.path.abspath(__file__))
		absolute_output_directory = os.path.join(my_directory,output_directory)
		
		# create folder
		if not os.path.exists(absolute_output_directory):
			try:
				os.makedirs(absolute_output_directory)
			except():
				print('Could not create directory', absolute_output_directory)
				return None

		file_name = os.path.join(absolute_output_directory, self.pmid + '.json')
		with open(file_name,'w') as f:
			f.write(	json.dumps(self.text[0], indent=2, separators=(',', ':')))
		
