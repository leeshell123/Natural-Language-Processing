'''
Created on 10/29/2013

@author: Xiao Li
''' 
import re
corpora=open('berp-POS-train.txt','r').read()

'''corporus with start and end tag'''
newcorp=re.sub(r'\n\n', '\n\end\t\end\n\n\start\t\start\n',corpora) 
pairs=[]
pairs.extend(re.split(r'[\n]+', newcorp))
pairDict={}
pairTuple=[]
tags=[]
tagDict={}
pairsset=set(pairs)

'''pairTuple store data like (i,prop)'''
for i in pairs:
    s = (tuple(re.split(r'[\t]', i)))
    pairTuple.append(s)
    
pairTupleSet = set(pairTuple)
    
'''pairDict store data like (i,prop):5'''
for i in pairTupleSet:
    pairDict[i]=pairTuple.count(i) 
    
for (u,v) in pairTuple:
    tags.append(v)

tagset=set(tags)
    
for i in tagset:
    tagDict[i]=tags.count(i)  
    
tagpair=[]
for i in range(0, (len(tags)-1)):
    s=tags[i],tags[i+1]
    tagpair.append(s)

tagpairSet=set(tagpair)

tagpairDict={}
for i in tagpairSet:
    tagpairDict[i]=tagpair.count(i)    

 
count=0
tagset={}
for i in tagDict:
    tagset[count]=i
    count=count+1
'''Deal with unknown words and store the new result with UNK in unkpairDict'''    
unkpairDict={}
for (u,v) in pairDict:
    if(pairDict[(u,v)]<=3):
        pair=('unk',v)
        if(unkpairDict.has_key(pair)==False):
            unkpairDict[('unk',v)]=pairDict[(u,v)]
        else:
            unkpairDict[('unk',v)]=unkpairDict[('unk',v)]+pairDict[(u,v)]

for(u,v) in pairDict:
    if(pairDict[(u,v)]>3):
        unkpairDict[(u,v)]=pairDict[(u,v)]
        
lexical=set()
for(u,v) in unkpairDict:
    if ((u in lexical)==False):
        lexical.add(u)
    
def unknownwords(origin):
    Observation=[]
    for i in origin:
        if((i in lexical)==False):
            Observation.append('unk')
        else:
            Observation.append(i)
            
    return Observation

class wordtag:
    def __init__ (self,word,tag,backpointer,maxpro):
        self.word=word
        self.tag=tag
        self.backpointer=backpointer
        self.maxpro=maxpro

def createTable(Observation):
    sentence=[]
    for i in range(0, len(Observation)):
        eachword=[]
        for t in range(0,38):
            m=wordtag(Observation[i],tagset[t],-1,0)
            eachword.append(m)
        sentence.append(eachword)
    return sentence





    


def Viterbi(origin):
    Observation=unknownwords(origin)
    sentence=createTable(Observation)
    for i in range(0, 38):
        pair=[Observation[0],tagset[i]]
        pair=tuple(pair)
        if(unkpairDict.has_key(pair)==False):
            sentence[0][i].maxpro=0
        else:
            '''+1 smoothing'''
            if(tagpairDict.has_key(('\\start', tagset[i]))==True):           
                transitionpro=float(tagpairDict[('\\start',sentence[0][i].tag)]+1)/float(unkpairDict[('\\start','\\start')]+37)
            else:
                transitionpro=1/(float(unkpairDict[('\\start','\\start')]+37))
            likelyhood=float(unkpairDict[pair])/float(tagDict[sentence[0][i].tag])
            sentence[0][i].maxpro=likelyhood*transitionpro

    for i in range(1, len(Observation)):
        for currentrowtag in range(0, 38):
            pair=[Observation[i],tagset[currentrowtag]]
            pair=tuple(pair)
            if(unkpairDict.has_key(pair)==False):
                pass
            else:
                for previousrowtag in range(0, 38):
                    if(tagpairDict.has_key((tagset[previousrowtag],tagset[currentrowtag]))==False):
                        '''+1 smoothing'''
                        transitionpro=1/float(tagDict[tagset[previousrowtag]]+37)
                    else:
                        transitionpro=float(tagpairDict[(tagset[previousrowtag],tagset[currentrowtag])]+1)/float(tagDict[tagset[previousrowtag]]+37)
                    likelyhood=float(unkpairDict[pair])/float(tagDict[tagset[currentrowtag]])
                    finalpro=transitionpro*likelyhood*sentence[i-1][previousrowtag].maxpro
                    if(sentence[i][currentrowtag].maxpro<finalpro):
                        sentence[i][currentrowtag].maxpro=finalpro                       
                        sentence[i][currentrowtag].backpointer=previousrowtag
    endpro=0
    endpointer=''
    for i in range(0, 38):
        if(tagpairDict.has_key((tagset[i],'\\end'))==False):
            '''+1 smoothing'''
            transitionpro=1/float(tagDict[tagset[i]]+37)
        else:
            transitionpro=float(tagpairDict[(tagset[i],'\\end')]+1)/float(tagDict[tagset[i]]+37)
        finalpro=transitionpro*sentence[len(sentence)-1][i].maxpro
        if(endpro<finalpro):
            endpro=finalpro                       
            endpointer=i
    backpointer=endpointer
    taggedlist=[]
    for i in range((len(sentence)-1),-1,-1):
        taggedpair=(origin[i],sentence[len(sentence)-1][backpointer].tag)
        backpointer=sentence[i][backpointer].backpointer
        taggedlist.insert(0,taggedpair)
    
    return taggedlist
        

testcorp=open('berp-POS-test-sentences.txt','r').read()
teststc=re.split(r'\n\n',testcorp)
testword=[]
for i in teststc:
    t=[]
    t=re.split(r'\n',i)
    testword.append(t)
    
result=[]
    
for s in testword:
    result.append(Viterbi(s))  
    
f=open('result.txt','w')
for i in result:
    for t in i:
        k=''.join([str(s) for s in t[0]])
        l=''.join([str(s) for s in t[1]])
        f.write(k+"\t"+l+"\n")
    f.write("\n")
f.close()

 

  
        
