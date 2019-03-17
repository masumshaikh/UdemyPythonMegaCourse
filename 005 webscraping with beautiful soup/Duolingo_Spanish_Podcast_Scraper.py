# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 16:45:52 2019

@author: e1081018
"""
import re
import requests
from bs4 import BeautifulSoup as Soup

class Duolingo_Episode:
    def __init__(self, url: str, proxies = None):
        self.soup = None # soup object containing the web page
        self.raw_title = None # title of episode as on web page
        self.transcript = None # the actual transcript
        self.spanish_only = None # spanish only
        self.all_p = None # soup of all <p> nodes
        
        r = requests.get(url, proxies = proxies)
        self.soup = Soup(r.content, 'lxml')
        self.set_raw_title()
    
    def set_raw_title(self):
        title = self.soup.find("h1", {"class":"entry-title"})
        self.raw_title = title.text[1:]
        
    def get_title(self):
        temp = re.sub("Episode ", "Duolingo Spanish Podcast E0", self.raw_title)
        return re.sub(r":", r" --", temp)
        
    def get_filename(self):
        temp = re.sub(r": ", "-", self.raw_title)
        temp = re.sub("Episode ", "DL-0", temp)
        return temp + ".txt"
    
    def get_filename_spanish(self):
        temp = re.sub(r": ", "-", self.raw_title)
        temp = re.sub("Episode ", "DL-0", temp)
        return temp + "-es_only.txt"
    
    def get_transcript(self):
        # Get the meat of the page
        entry_content = self.soup.find("div", {'class':'entry-content'})
        
        # Load all the <p> tags
        self.all_p = entry_content.find_all("p")
        
        # Function to check if a tag contains the tag <strong>
        def contains_strong(tag):
            return 'strong' in [child.name for child in tag.children]
        
        # Get list of those <p> which contain <strong>
        # That's just due to the structure of the page in question.
        transcript = [p.text for p in self.all_p if contains_strong(p)]
        self.transcript = " \n\n".join(transcript)
        return self.transcript
    
    def get_spanish_only(self):
        # Find names of people other than Martina
        strong = self.soup.find_all("strong")
        other_names = [t.text for t in set(strong) if not ('Martina' in t.text)]
        
        def not_martina(tag):
            for name in other_names:
                if name in tag.text:
                    return True
            return False
        
        pattern = "(" + "|".join(other_names) +")"
        spanish_only = [re.sub(pattern,"", p.text) for p in self.all_p if not_martina(p)]
        self.spanish_only = " \n".join(spanish_only)
        return self.spanish_only
    
if __name__ == '__main__':
    urls = ["http://podcast.duolingo.com/episode-21-la-nana-the-nanny", \
            "http://podcast.duolingo.com/episode-22-autostop-en-afganistan-hitchhiking-in-afghanistan", \
            "http://podcast.duolingo.com/episode-23-el-regalo-the-gift" , \
            "http://podcast.duolingo.com/episode-24-mis-dos-papas-my-two-dads", \
            "http://podcast.duolingo.com/episode-25-el-rescatado-the-rescued"]
    
    for url in urls:
        tr = Duolingo_Episode(url)
        
        with open(tr.get_filename(), "w") as the_file:
            the_file.write(tr.get_title())
            the_file.write("\n\n")
            the_file.write(tr.get_transcript())
        
        with open(tr.get_filename_spanish(), "w") as the_file:
            the_file.write(tr.get_spanish_only())

    
        
    print(ep21.get_title())
    print(ep21.get_filename())
    print(ep21.get_filename_spanish())