# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import re
import json

def main():
    paragraphs = list()
    with open('rules.json') as rules:
        rules = rules.read()
        rules = json.loads(rules)
    keywords = {category: [re.compile(r) for r in rules[category]] for category in rules.keys()}

    with open("examples/github.tos") as file:
        for paragraph in file:
            paragraph = paragraph.split(".")
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
                paragraphs.append(sentence)

    tagged = 0.0
    other = 0.0
    for sentence in paragraphs:
        if len(sentence[2])>0:
            tagged+=1
        else:
            other+=1
    print (tagged/other)*100
        
main()
