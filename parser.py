#a vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

#------------------------------------------------------------------
# parser.py
#
# Created by: Samuel Chrisinger, Canar Uguz, Fabian von Feilitzsch
#
# This is the main script for parsing the Terms of Service 
# documents for the clierly webapp. 
#
# It reads a json file of rules from the file 'rules.json', where 
# each rule is specified as a category associated with a list of
# regular expressions.
#
# It then recieves a string of input text. The string is broken 
# into paragraphs, which contain a list of tuples. Each tuple is 
# of the form (sentence text, set of matcheed keywords, set of 
# matched categories). 
#
# The list of paragraphs is the return value.
#------------------------------------------------------------------

import re
import json

def parse(text):
    paragraphs = list()

    # Reads in the rules
    with open('rules.json') as rules:
        rules = rules.read()
        rules = json.loads(rules)

    # Creates a dict of Category:[keyword] pairs, compiling the keyword regexps
    keywords = {category: [re.compile(r) for r in rules[category]] for category in rules.keys()}

    # Matches substrings in each sentence to the keyword regular expressions
    text = text.split('\n')
    for paragraph in text:
        paragraph = paragraph.split(". ")
        p_list = list()
        for sentence in paragraph:
            sentence = sentence.strip()
            flags = set()
            categories = set()
            for key in keywords.keys():
                for keyword in keywords[key]:
                    if (keyword.search(sentence)):
                        flags.add(keyword.pattern)
                        categories.add(key)
            sentence = (sentence, flags, categories)            
            p_list.append(sentence)
        paragraphs.append(p_list)
    return paragraphs
