# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 17:54:38 2019

@author: e1081018
"""

import re
import requests
from bs4 import BeautifulSoup as Soup

def get_soup(url, proxies = None):
    r = requests.get(url, proxies = proxies)
    return Soup(r.content, 'html.parser')

def get_all_url_links(proxies = None):
    url = "https://slowgerman.com/inhaltsverzeichnis/"
    soup = get_soup(url, proxies)
    all_links = soup.find("ul", {"class":"lcp_catlist"}).find_all("li")
    return [link for link in all_links if "SG #" in link.text]

def create_dicts(proxies = None):
    all_link_tags = get_all_url_links(proxies)
    all_links = [tag.find("a")['href'] for tag in all_link_tags]
    all_titles = [link.text.strip() for link in all_link_tags]
    indices = [int(re.search(r"(?<=#).*?(?=\:)", title).group()) for title in all_titles]
    
    if(len(all_links) == len(all_titles) and len(all_links) == len(indices)):
        dict_links  = {indices[i]:all_links[i] for i in range(len(all_links))}
        dict_titles = {indices[i]:all_titles[i] for i in range(len(all_links))}        
        return (dict_links, dict_titles)

def get_transcript(url, proxies = None):
    soup = get_soup(url, proxies)
    temp = (soup.find("div", {"class":"entry-content"})).text
    for i in range(5):
        temp = re.sub(r"\n\n", r"\n", temp)
    temp = re.sub(r"\n", r" \n\n", temp)
    return temp

def get_filename(title):
    temp = re.sub(r"SG #(\d+): ", r"SG\1-", title) + ".txt"
    temp = re.sub("/", "or", temp)
    return temp

proxies = {'http': 'http://localhost:3128', 'https': 'https://localhost:3128'}
dict_links, dict_titles = create_dicts(proxies)    
for i in range(180,182):
    print(get_filename(dict_titles[i]))
    with open(get_filename(dict_titles[i]), "w") as the_file:
        the_file.write(dict_titles[i])
        the_file.write(get_transcript(dict_links[i], proxies))
