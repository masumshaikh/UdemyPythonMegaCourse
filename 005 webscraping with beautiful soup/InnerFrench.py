# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 14:55:54 2019

@author: e1081018

Does not get soup directly from web:
    need to download html from browser to working directory
"""
import os
from bs4 import BeautifulSoup as Soup

def get_soup(filename):
    with open(filename, "r", encoding="utf8") as in_file:
        r = in_file.read()
    return Soup(r, 'html.parser')

def get_outfile_name(filename):
    return filename.replace('#', 'IF_0').replace(' -.html', '.txt')

def print_trancript(filename_in):
    soup = get_soup(filename_in)
    filename_out = get_outfile_name(filename_in)
    content = soup.find("div", {"class":"elementor-text-editor elementor-clearfix"})
    paras = content.find_all("p")
    with open(filename_out, "w", encoding="utf8") as out_file:
        for para in paras:
            out_file.write(para.text + " \n \n")

html_files = [file for file in os.listdir() if file.endswith('.html')]
for file in html_files:
    print (file)
    print_trancript(file)