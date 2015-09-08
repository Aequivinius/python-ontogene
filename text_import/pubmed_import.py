#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nico Colic, July 2015
# Based on code by Tilia Ellendorff

import helpers
from article import Article

from Bio import Entrez

import pickle # Python 3 will automatically try to use cPickle
import os
import time

dump_directory = 'dumps'

def Pubmed_import(pmid, pubmed_email=None, dump_directory_absolute=None, options=None, args=None):
	"""pubmed_email is used to download, not necessary if you only load previously downloaded files. options and args are for downloading from pubmed. Use dump_directory_absolute to provide your own path to dump_directory, if necessary. 
	
	Pubmed will return files in biopython format, which we convert into our article format."""
	
	# setting up dump directory (in case the user might have specified his own directory)
	if dump_directory_absolute:
		my_dump_directory = helpers.make_directory(dump_directory_absolute)
	else:
		my_dump_directory = os.path.join(os.path.dirname(__file__),dump_directory)		
	dump_file = os.path.join(my_dump_directory,pmid)
	
	# check if pickle exists in dump_directory
	if not pmid in os.listdir(my_dump_directory): # download
		print('ATTEMPT TO DOWNLOAD DATA FOR', pmid)
		try:
		    record = download_biopython(pmid, pubmed_email, options=options, args=args)
		    pickle_biopython(record, dump_file)
		except:
		    print('Couldn\'t download ' , pmid)
		    return None
		finally:
		    time.sleep(0.333) # to prevent too many downloads to pmid, which will get you blocked
		print('DOWNLOADED AND WRITTEN TO FILE')
	
	else: # load from file
		try:
			record = pickle.load(open(dump_file,'rb'))

		except (IOError, EOFError, AttributeError):
			print('ERROR, NO DATA FOR', pmid)
			return None
				
	article = biopython_to_article(pmid,record)
	return article	

def download_biopython(pmid, pubmed_email, options=None, args=None):

    if pubmed_email == None:
        print('DOWNLOAD OF NEW DATA CANNOT BE COMPLETED, PLEASE GIVE YOUR EMAIL IN CONFIG.PY.')
        return None

    Entrez.email = pubmed_email
    print('THE DATA FOR PUBMED-ID', pmid, 'WILL BE DOWNLOADED')

    handle = Entrez.efetch(db="pubmed", id=pmid, retmode="xml")
    biopython_record = Entrez.read(handle)
    return biopython_record
   
def pickle_biopython(record,dump_file):
	with open(dump_file, 'wb') as f:
		
		# TODO: find out why it only works when I use protocol=1
		pickle.dump(record,f,protocol=1)

def biopython_to_article(pmid,record):	
	article = Article(pmid)
	article.add_section('title', get_title(record))
	article.add_section('abstract',get_abstract(record))
	
	# i think here's were the interesting bit starts

def get_abstract(record):
	try:
	    text_dict = record[0]
	    abstract = text_dict[u'MedlineCitation'][u'Article'][u'Abstract'][u'AbstractText']
	    if len(abstract) == 1:
	        return ' '.join(abstract)

	    else:
	        # copied from Tilia 24.7.2015, and adapted for Python3
	        abstract_list = []
	        for i in range(len(abstract)):
	            one_abstract_section = abstract[i]
	            one_abstract_section_string = str(abstract[i])
	            # print(one_abstract_section_string)
	            one_abstract_section_attr = one_abstract_section.attributes
	            # print(one_abstract_section_attr)

	            try:
	                # Add abstract headings, such as BACKGROUND; make this optional?

	                abstract_label = one_abstract_section_attr[u'Label']
	                new_abstract_section_string = abstract_label + ': ' + one_abstract_section_string

	                # if not new_abstract_section_string.endswith(u'.'):
#                             new_abstract_section_string = new_abstract_section_string + u'.'

	                # print(new_abstract_section_string)
	                # print('\n')
	                abstract_list.append(new_abstract_section_string)
	            except KeyError:
	                abstract_list.append(one_abstract_section_string)

	        #abstract_list = [unicode(abstract[i]) for i in range(len(abstract))]

	        abstract_string = ' '.join(abstract_list)
	        return abstract_string

	except (IndexError, KeyError, AttributeError):
	    return None

def get_title(record):
    try:
        text_dict = record[0]
        return str(text_dict[u'MedlineCitation'][u'Article'][u'ArticleTitle'])

    except (IndexError, KeyError, AttributeError):
        return None
# 
#     def get_mesh(self, options=None, args=None):
#         try:
#             text_dict = self.text[0]
#             mesh_list = text_dict[u'MedlineCitation'][u'MeshHeadingList']
#             descriptor_list = [str(mesh_list[i][u'DescriptorName']) for i in range(len(mesh_list))]
#             descriptor_dict = dict((n, descriptor_list[n]) for n in range(len(descriptor_list)))
# 
#             qualifier_list = dict((i, [str(item) for item in mesh_list[i][u'QualifierName']]) for i in range(len(mesh_list)))
#         except (IndexError, KeyError):
#             return None
# 
#     def get_mesh_descriptors(self, options=None, args=None):
#         try:
#             text_dict = self.text[0]
#             mesh_list = text_dict[u'MedlineCitation'][u'MeshHeadingList']
#             descriptor_list = [str(mesh_list[i][u'DescriptorName']) for i in range(len(mesh_list))]
#             return '; '.join(descriptor_list)
#         except (IndexError, KeyError):
#             return None
# 
# 
#     def get_mesh_qualifiers(self, options=None, args=None):
#         try:
#             text_dict = self.text[0]
#             mesh_list = text_dict[u'MedlineCitation'][u'MeshHeadingList']
#             qualifier_list = list(set(sum([[unicode(item) for item in mesh_list[i][u'QualifierName']] for i in range(len(mesh_list))], [])))
#             return '; '.join(qualifier_list)
#         except (IndexError, KeyError):
#             return None
# 
#     def get_whole_abstract(self, options=None, args=None):
#         try:
#             whole_abstract_list = []
#             # whole_abstract_list.append(self.pmid + '. ')
#             whole_abstract_list.append(self.get_title())
#             whole_abstract_list.append(self.get_abstract())
# 
#             if not self.get_mesh_descriptors() == None:
#                 whole_abstract_list.append(self.get_mesh_descriptors())
# 
#             return ' '.join(whole_abstract_list)
# 
#         except (IndexError, KeyError, TypeError):
#             return None
# 
#     def get_whole_abstract_minus_mesh(self, options=None, args=None):
#         try:
#             whole_abstract_list = []
#             # whole_abstract_list.append(self.pmid + '. ')
#             whole_abstract_list.append(self.get_title())
#             whole_abstract_list.append(self.get_abstract())
# 
#             return ' '.join(whole_abstract_list)
# 
#         except (IndexError, KeyError, TypeError):
#             return None
#
#     def export_xml(self,output_directory,mode=None):
#         import xml.etree.ElementTree as ET
#         pmid_medline = self.text[0][u'MedlineCitation']
#         
#         # BUILDING THE TREE
#         try:
#             article = ET.Element('article')
#             article_attributes = {	'id':'',
#                                     'pmid':pmid_medline[u'PMID'],
#                                     'type':pmid_medline[u'Article'][u'PublicationTypeList'][0],
#                                     'year':pmid_medline[u'DateCompleted'][u'Year']
#                                     };
#             if u'ISSN' in pmid_medline[u'Article'][u'Journal']:
#                 article_attributes['issn'] = pmid_medline[u'Article'][u'Journal'][u'ISSN']
#             for attribute, value in article_attributes.items():
#                 article.set(attribute,value)
#             
#             article_title = ET.SubElement(article,'article_title')
#             article_title.set('id','')
#             article_title.set('type','Title')
#             article_title.text = pmid_medline[u'Article'][u'ArticleTitle']
#             
#             abstract = ET.SubElement(article,'abstract')
#             abstract.set('id','')
#             abstract.set('type','')
#             abstract.text = pmid_medline[u'Article'][u'Abstract'][u'AbstractText'][0]
#             
#             if u'ChemicalList' in pmid_medline:
#                 chemicals = ET.SubElement(article,'chemicals')
#                 chemicals.set('id','')
#                 for chemical in pmid_medline[u'ChemicalList']:
#                     c = ET.SubElement(chemicals, 'chemical')
#                     c.set('UI',chemical[u'NameOfSubstance'].attributes[u'UI'])
#                     c.set('RegistryNumber',chemical[u'RegistryNumber'])
#                     c.text = chemical[u'NameOfSubstance']
#             
#             mesh = ET.SubElement(article,'mesh')
#             mesh.set('id','')
#             for mesh_element in pmid_medline[u'MeshHeadingList']:
#                 m = ET.SubElement(mesh, 'm')
#                 m.text = mesh_element[u'DescriptorName']
#                 m.set('UI',mesh_element[u'DescriptorName'].attributes[u'UI'])
#                 major_topic = mesh_element[u'DescriptorName'].attributes[u'MajorTopicYN']
#                 m.set('MajorTopicYN',major_topic)
#             
#                 qualifier_name = mesh_element[u'QualifierName']
#                 if qualifier_name != []:
#                     m.set('qualifier_name',qualifier_name[0])
#                     m.set('qualifier_name_UI',qualifier_name[0].attributes[u'UI'])
#                     qualifier_name_major_topic = qualifier_name[0].attributes[u'MajorTopicYN']
#                     if major_topic != qualifier_name_major_topic:
#                         m.set('qualifier_name_major_topic',qualifier_name_major_topic)
#         
#         except LookupError as error:
#             print('Tree could not be build, possibly because Pubmed data is in an unexpected format.')
#             print(error)
#             return
#                         
#         # preparing writing to file
#         my_directory = self.make_output_subdirectory(output_directory)
#         
#         # write using etree
#         file_name = os.path.join(my_directory, self.pmid + '.xml')
#         if ( mode == 'both' or mode == 'normal' ):
#             with open(file_name,'wb') as f:
#                 ET.ElementTree(article).write(f,encoding="UTF-8",xml_declaration=True)
#         
#         # Pretty Print
#         file_name = os.path.join(my_directory, self.pmid + '_pretty.xml')
#         if ( mode == 'both' or mode == 'pretty' or mode == None ) :
#             from xml.dom import minidom
#             
#             pretty_article = minidom.parseString(ET.tostring(article, 'utf-8')).toprettyxml(indent="	")
#             with open(file_name,'w') as f:
#                 f.write(pretty_article)
#     
#     def export_json(self,output_directory):
#         import json
#         
#         my_directory = self.make_output_subdirectory(output_directory)
# 
#         file_name = os.path.join(my_directory, self.pmid + '.json')
#         with open(file_name,'w') as f:
#             f.write(	json.dumps(self.text[0], indent=2, separators=(',', ':')))
#                 
#     def get_absolute_directory(self,directory):
#         my_directory = os.path.dirname(os.path.abspath(__file__))
#         return os.path.join(my_directory, self.dump_directory)
#         
#     def make_output_subdirectory(self,output_directory_absolute):
#         my_directory = os.path.join(output_directory_absolute, 'text_import')
#         return self.make_directory(my_directory)
#                         
# 
# 
# 