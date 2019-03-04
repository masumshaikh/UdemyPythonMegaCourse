# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 22:17:10 2019

@author: e1081018
"""
import json
import difflib

class DefinitionsHelper:
    msg_not_found = "That word does not exist in the dictionary"
    msg_close_matches_found = "That exact word couldn't be found! Here are some suggestions:\n"
    
    def __init__(self):
        self.definitions = dict()
    
    def __str__(self):
        if not self.definitions:
            return self.msg_not_found

        else:
            if (len(self.definitions) == 1):
                ans = ""
            else:
                ans = self.msg_close_matches_found
                ans += "\n" + ", ".join(self.definitions.keys()) + "\n"
            
            for k in self.definitions.keys():
                ans += '\n{}:'.format(k)
                count = 1
                for v in self.definitions[k]:
                    ans += '\n{}.\t{}\n'.format(count, str(v))
                    count += 1
            return ans
        
    def add(self, word, definition):
        self.definitions[word] = definition
    
    def clear(self):
        self.definitions = {}

class DictApp:
    
    def __init__(self):      
        with open ("data.json", "r") as myfile:
            self.dictionary = json.load(myfile) 
            
            # todo: what if key clashes in dictionary? eg US and us
            all_words_lower = [w.lower() for w in self.dictionary.keys()] 
            self.normalised_words = dict( \
                                    zip(all_words_lower, self.dictionary.keys()))
            
    def try_get_definitions(self, word):
        definitions = DefinitionsHelper()
        
        if (word.lower() in self.normalised_words):
            orig_word = self.normalised_words[word.lower()]
            definitions.add(orig_word, self.dictionary[orig_word])
        else:
            close_matches = difflib.get_close_matches(word.lower(), \
                                                      self.normalised_words)
            close_matches += difflib.get_close_matches(word, \
                                                      self.dictionary)
            if close_matches:
                for match in close_matches:
                    definitions.add(match, self.dictionary[match])

        return definitions
    
    def main(self):
        word = "init"
        while (word != "x"):
            word = input (r"Enter a word (or 'x' to quit): ")
            if (word != "x"):
                print(self.try_get_definitions(word))
                
if __name__ == "__main__":
    DictApp().main()