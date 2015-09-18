#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nico Colic, September 2015
# Based on code by Tilia Ellendorff

import helpers
from article import Article

from Bio import Entrez

import pickle # Python 3 will automatically try to use cPickle
import os
import time

dump_directory = 'dumps'

def pubmed_import(pmid, pubmed_email=None, dump_directory_absolute=None, options=None, args=None):
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
		pickle.dump(record,f,protocol=1)

def biopython_to_article(pmid,record):
	article = Article(pmid)
	
	article.add_section('title', get_title(record))
	for name , abstract in get_abstracts(record).items():
		article.add_section(name,abstract)
	
	# add meta data if it can be found
	try:
		article.set_mesh(get_mesh(record))
	except:
		pass
		
	try:
		article.type_ = get_type(record)
	except:
		pass
	
	try:
		article.year = get_year(record)
	except:
		pass
	
	return article

def get_abstracts(record):
	"""Returns a dictionary with abstracts. Normally this will be 'abstract':'text', but because some articles have multiple abstracts or sections such as 'background'"""
	text_dict = record[0]
	abstracts = dict()
	
	# check different possible locations for abstract
	try: 
		abstracts['Abstract'.lower()] = text_dict[u'MedlineCitation'][u'Article'][u'Abstract'][u'AbstractText']	
	except (IndexError, KeyError, AttributeError):
		pass
		
	try: 
		abstracts['OtherAbstract'.lower()] = text_dict[u'MedlineCitation'][u'OtherAbstract'][0][u'AbstractText']
	except (IndexError, KeyError, AttributeError):
		pass
	
	# abstract fields may contain subsections, which we extract here
	for name , abstract in abstracts.items():
		if len(abstract) > 1:
			for i in range(len(abstract)):
				label = abstract[i].attributes[u'Label']
				abstracts[label.lower()] = str(abstract[i])
			
			del abstracts[name]
		else:
			abstracts[name] = abstract[0]
	
	return abstracts
	
def get_title(record):
    try:
        text_dict = record[0]
        return str(text_dict[u'MedlineCitation'][u'Article'][u'ArticleTitle'])

    except (IndexError, KeyError, AttributeError):
        return None

def get_mesh(record):
    try:
        text_dict = record[0]
        mesh_list = text_dict[u'MedlineCitation'][u'MeshHeadingList']
        descriptor_list = [str(mesh_list[i][u'DescriptorName']) for i in range(len(mesh_list))]
        # descriptor_dict = dict((n, descriptor_list[n]) for n in range(len(descriptor_list)))
        # qualifier_list = dict((i, [str(item) for item in mesh_list[i][u'QualifierName']]) for i in range(len(mesh_list)))
        return descriptor_list
    except (IndexError, KeyError):
        return None
        
def get_type(record):
	return str(record[0][u'MedlineCitation'][u'Article'][u'PublicationTypeList'][0])
	
def get_year(record):
	return record[0][u'MedlineCitation'][u'DateCompleted'][u'Year']
