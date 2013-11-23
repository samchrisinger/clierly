#vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

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
#
import re
import json

def parse(text):
    paragraphs = list()

    # Reads in the rules
    with open('rules.json') as f:
        f = f.read()
        js = json.loads(f)
        rules = js['rules']
        excludes = js['exclusions']

    # Creates a dict of Category:[keyword] pairs, compiling the keyword regexps
    keywords = {category: [re.compile(r) for r in rules[category]] for category in rules.keys()}
    excludes = [re.compile(r) for r in excludes]
    print(keywords.keys())

    # Matches substrings in each sentence to the keyword regular expressions
    text = text.split('\n')
    for paragraph in text:
        paragraph = paragraph.split(". ")
        p_list = list()
        for sentence in paragraph:
            sentence = sentence.strip()
            flags = set()
            categories = set()
            exclude = False
            for e in excludes:
                if e.search(sentence):
                    exclude = True
                    break
            if exclude:
               sentence = (sentence, flags, message)
               p_list.append(sentence)
               break
            for key in keywords.keys():
                for keyword in keywords[key]:
                    if (keyword.search(sentence)):
                        flags.add((key, keyword.pattern))
                        #flags.add(keyword.pattern)
                        #categories.add(key)
            #message = _generateMessage(flags, categories)
            #sentence = (sentence, flags, categories, message)            
            message = _generateMessage(flags)
            flags = [f[0] for f in flags]
            sentence = (sentence, flags, message)
            p_list.append(sentence)
        paragraphs.append(p_list)
    return paragraphs

# Helper function to generate error messages based on categories and flags
def _generateMessage(flags):
    flags = list(flags)
    CHANGE = ['Change']
    VIOLATION = ['Violation','Termination', 'Restrictions']
    CONTENT = ['Content', 'Deactivation']
    RISK = ['Risk','Arbitration','Consent', 'Restrictions']
    PERSONALINFO = ['PersonalInformation','Security', 'Restrictions']
    MONEY = ['Money']
    message = ''
    for flag in flags:
        category = flag[0]
        flag = flag[1]
        if(category in CHANGE):
            message += 'The service may have a right to change terms here. '
            message += '\n'
        elif(category in VIOLATION):
            message += 'The service considers this behavior a violation of terms. '
            if(category == 'Termination'):
                message += 'This violation may be punished by disruption of service. '
            elif(flag == 'must\sbe'):
                message += 'Make sure you satisfy the requirement listed here. '
            message += '\n'
        elif(category in CONTENT):
            message += 'This section details the rights you have to your own content and the content of others. '
            if (category == 'Deactivation'):
                message += 'It also details what happens to your information when you account is closed. '
                #TODO: see if we can figure out what happens to content (deleted or stored + rights)
            message += '\n'
        elif(category in RISK):
            message += 'You are agreeing to assume risk here'
            if(category == 'Arbitration'):
                message += '- and lawyers are involved'
            elif(category == 'Restrictions'):
                message += '. Make sure you know exactly what you are consenting to'
            message += '. \n'
        elif(category in PERSONALINFO):
            message += 'This section concerns you personal information. '
            if (category == 'PersonalInformation'):
                message += 'Make sure that you are comfortable giving away this information. '
            elif(category == 'Security'):
                message += 'Make sure that they are storing your information securely. '
            elif(category == 'Consent'):
                message += 'Make sure that sensitive information is only shared with third-parties you trust.'
            message += '\n'
        elif(category in MONEY):
            message += 'This is part of your financial agreement with the service. Make sure you understand how, why, and when you will be charged. '
            message += '\n'
    return message
    
