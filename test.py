#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nico Colic, September 2015

import article

# my_article = article.Article("123")
# 
# my_section = article.Section("s123","title","mine section is lamdamm")
# my_section.add_subelement(article.Token("token123","tokentext"))
# my_article.add_subelement(my_section)
# 
# print(my_article)

from text_import.pubmed_import import Pubmed_import

# article = Pubmed_import("12345678","ncolic@gmail.com") 
article = Pubmed_import("12346789","ncolic@gmail.com")
article.print_xml('/Users/Qua/Downloads/asn.xml',pretty_print=1)
