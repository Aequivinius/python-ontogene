#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nico Colic, September 2015

import article

my_article = article.Article("123")

my_section = article.Section("s123","title","mine section is lamdamm")
my_section.add_subelement(article.Token("token123","tokentext"))
my_article.add_subelement(my_section)

print(my_article)

