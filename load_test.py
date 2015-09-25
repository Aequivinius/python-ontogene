#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nico Colic, September 2015

import article

my_article = article.Article.unpickle('/Users/Qua/Downloads/test/10030003.pickle')
my_article.print_entities_xml('/Users/Qua/Downloads/test/10030003_entities.xml',pretty_print=True)
