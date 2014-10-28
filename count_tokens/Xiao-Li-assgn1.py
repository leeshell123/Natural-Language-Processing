'''


@author: Xiao
'''
import re



def splitToPara(article):
    return re.split(r'[\t\n]*', article)
    
def splitToSentence(para):
    return re.split(r'(?<!Dr)(?<!Ms)(?<!Mr)(?<!Miss)(?<![A-Z].[A-Z])[.?!][")]*[\s]+|[A-Z].[A-Z].[\s]+[A-Z][a-z]', para)
    
def splitToToken(sentence):
    return re.split(r'["):,;-]*[.?!]*[\s]*["):,;-]*[\s]+[-"(]*',sentence)
    
    
def AnalyzeArticle(article):
    allsentences=[]
    alltokens=[]
    paras=splitToPara(article)
    print "The paragraph number is ", len(paras)
    
    for para in paras:
        allsentences.extend(splitToSentence(para))
    
    for sentence in allsentences:
        alltokens.extend(splitToToken(sentence))
        
    print "The sentence number is ", len(allsentences)
    print "The token number is ", len(alltokens)
    for t in allsentences:
        print t
        print '\n'
    
    
article=open('nlptest.txt','r').read()

AnalyzeArticle(article)    
    





























