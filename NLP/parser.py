# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import re

url = '''/((([A-Za-z]{3,9}:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]+|(?:www.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+)((?:\/[\+~%\/.\w-_]*)?\??(?:[-\+=&;%@.\w_]*)#?(?:[\w]*))?)/'''

keywords = {'Reference':[re.compile(a) for a in ['Section', 'see.*below', 'link']],\
'Change':[re.compile(a) for a in ['changes?', 'amend(ment)?', 'alteration', 'addition', 'new\sfeatures', 'modify', 'without\snotice']],\
 'Consent':[re.compile(a) for a in ['consent', 'accept', 'third[\s\-]?party']],\
 'Violation':[re.compile(a) for a in ['violation','not\spermitted','unauthorized', 'illegal','unlawful','abuse','excessive']],\
 'Termination':[re.compile(a) for a in ['termination', 'cancellation','loss\sof\sservice', 'suspension', 'discontinue','terminate']],\
 'Deactivation':[re.compile(a) for a in ['deactivate']],\
 'Content':[re.compile(a) for a in ['content', 'Content', 'do\snot\sdelete', 'forfeit', 'relinquish','(intellectual)?\sproperty\s(rights)?', 'screen']],\
 'Risk':[re.compile(a) for a in ['(own\s)?risk', 'cannot\sbe\s(held\s)?responsible', '((can)|(will\s))?not\sbe\s(held)?\sliable', 'loss\sof']],\
 'Restrictions':[re.compile(a) for a in ['must\sbe']],\
 'Personal Information':[re.compile(a) for a in ['((full)|(legal)\s)name','(e(\-)?mail\s)?address', 'personal','credit\scard','social\ssecurity(\snumber)?','(ssn)|(SSN)', 'must\senter']],\
 'Security':[re.compile(a) for a in ['security','password','encrypted']],\
 'Money':[re.compile(a) for a in ['charges', 'bill((ing)|(ed))?', 'pay(ment)?', '(non\-)?refund(able)?', 'credit((able)|s|(ed))', '(pro(\-)?)?rate(d)?']],\
 'Arbitration':[re.compile(a) for a in ['attorney','suit','settlement','claim','proceeding']]}

def main():
    paragraphs = list()
    with open("examples/github.tos") as file:
        for paragraph in file:
            paragraph = paragraph.split(".")
            for sentence in paragraph:
                sentence = sentence.strip()
                flags = list()
                categories = list()
                for key in keywords.keys():
                    for keyword in keywords[key]:
                        if (keyword.search(sentence)):
                            flags.append(keyword.pattern)
                            categories.append(key)
                sentence = (sentence, flags, categories)            
                paragraphs.append(sentence)
    for sentence in paragraphs:
        if len(sentence[2])>0:
            print str(sentence[0])+" : "+str(sentence[1])
        
main()
