import re
import math
corpora=open('gene.trainnew.txt','r').read()

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
words=[];
for (u,v) in pairTuple:
    words.append(u);

wordset=set(words);
wordDict={}
for i in wordset:
    wordDict[i]=words.count(i)

unkpairDict={}

for (u,v) in pairDict:
    if(wordDict[u]<3):
        if(len(u)>9):
            pairs=('unknown6',v)
            if(unkpairDict.has_key(pairs)):
                unkpairDict[('unknown6',v)]=unkpairDict[('unknown6',v)]+pairDict[(u,v)]
            else:
                unkpairDict[('unknown6',v)]=pairDict[(u,v)]
        elif(u.isdigit()):
            pairs=('unknown1',v)
            if(unkpairDict.has_key(pairs)):
                unkpairDict[('unknown1',v)]=unkpairDict[('unknown1',v)]+pairDict[(u,v)]
            else:
                unkpairDict[('unknown1',v)]=pairDict[(u,v)]
        elif(u.isalpha and u.isupper()):
            pairs=('unknown2',v)
            if(unkpairDict.has_key(pairs)):
                unkpairDict[('unknown2',v)]=unkpairDict[('unknown2',v)]+pairDict[(u,v)]
            else:
                unkpairDict[('unknown2',v)]=pairDict[(u,v)]
        elif(u.isalpha()):
            pairs=('unknown3',v)
            if(unkpairDict.has_key(pairs)):
                unkpairDict[('unknown3',v)]=unkpairDict[('unknown3',v)]+pairDict[(u,v)]
            else:
                unkpairDict[('unknown3',v)]=pairDict[(u,v)]
        elif(u.isalnum()):
            pairs=('unknown4',v)
            if(unkpairDict.has_key(pairs)):
                unkpairDict[('unknown4',v)]=unkpairDict[('unknown4',v)]+pairDict[(u,v)]
            else:
                unkpairDict[('unknown4',v)]=pairDict[(u,v)]
        else:
            pairs=('unknown5',v)
            if(unkpairDict.has_key(pairs)):
                unkpairDict[('unknown5',v)]=unkpairDict[('unknown5',v)]+pairDict[(u,v)]
            else:
                unkpairDict[('unknown5',v)]=pairDict[(u,v)]
    else:
        unkpairDict[(u,v)]=pairDict[(u,v)]



        
lexical=set()
for(u,v) in unkpairDict:
    if ((u in lexical)==False):
        lexical.add(u)
    
def unknownwords(origin):
    Observation=[]
    for i in origin:
        if((i in lexical)==False):
            if(len(u)>9):
                Observation.append('unknown6')                
            elif(u.isdigit()):
                Observation.append('unknown1')
            elif(u.isalpha and u.isupper()):
                Observation.append('unknown2')
            elif(u.isalpha()):
                Observation.append('unknown3')
            elif(u.isalnum()):
                Observation.append('unknown4')
            else:
                Observation.append('unknown5')
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
        for t in range(0,5):
            m=wordtag(Observation[i],tagset[t],-1,-float('inf'))
            eachword.append(m)
        sentence.append(eachword)
    return sentence

def Viterbi(origin):
    Observation=unknownwords(origin)
    sentence=createTable(Observation)
    for i in range(0, 5):
        pair=[Observation[0],tagset[i]]
        pair=tuple(pair)
        if(unkpairDict.has_key(pair)==False):
            sentence[0][i].maxpro=-float('inf')
        else:
            '''+1 smoothing'''
            if(tagpairDict.has_key(('\\start', tagset[i]))==True):           
                transitionpro=float(tagpairDict[('\\start',sentence[0][i].tag)]+1)/float(unkpairDict[('\\start','\\start')]+4)
                transitionpro=math.log(transitionpro)
            else:
                transitionpro=1/(float(unkpairDict[('\\start','\\start')]+4))
                transitionpro=math.log(transitionpro)
            likelyhood=float(unkpairDict[pair])/float(tagDict[sentence[0][i].tag])
            likelyhood=math.log(likelyhood)
            sentence[0][i].maxpro=likelyhood+transitionpro

    for i in range(1, len(Observation)):
        for currentrowtag in range(0, 5):
            pair=[Observation[i],tagset[currentrowtag]]
            pair=tuple(pair)
            if(unkpairDict.has_key(pair)==False):
                pass
            else:
                for previousrowtag in range(0, 5):
                    if(tagpairDict.has_key((tagset[previousrowtag],tagset[currentrowtag]))==False):
                        '''+1 smoothing'''
                        transitionpro=1/float(tagDict[tagset[previousrowtag]]+4)
                        transitionpro=math.log(transitionpro)
                    else:
                        transitionpro=float(tagpairDict[(tagset[previousrowtag],tagset[currentrowtag])]+1)/float(tagDict[tagset[previousrowtag]]+4)
                        transitionpro=math.log(transitionpro)
                    likelyhood=float(unkpairDict[pair])/float(tagDict[tagset[currentrowtag]])
                    likelyhood=math.log(likelyhood)
                    finalpro=transitionpro+likelyhood+sentence[i-1][previousrowtag].maxpro
                    if(sentence[i][currentrowtag].maxpro<finalpro):
                        sentence[i][currentrowtag].maxpro=finalpro                       
                        sentence[i][currentrowtag].backpointer=previousrowtag
    endpro=-float('inf')
    endpointer=''
    for i in range(0, 5):
        if(tagpairDict.has_key((tagset[i],'\\end'))==False):
            '''+1 smoothing'''
            transitionpro=1/float(tagDict[tagset[i]]+4)
        else:
            transitionpro=float(tagpairDict[(tagset[i],'\\end')]+1)/float(tagDict[tagset[i]]+4)
        transitionpro=math.log(transitionpro)
        finalpro=transitionpro+sentence[len(sentence)-1][i].maxpro
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

testcorp=open('officialtest.txt','r').read()
teststc=re.split(r'\n\n',testcorp)
testword=[]
for i in teststc:
    t=[]
    t=re.split(r'\n',i)
    testword.append(t)
    
result=[]
    
for s in testword:
    result.append(Viterbi(s))  
    
f=open('officialresult_feature1.txt','w')
for i in result:
    for t in i:
        k=''.join([str(s) for s in t[0]])
        l=''.join([str(s) for s in t[1]])
        f.write(k+"\t"+l+"\n")
    f.write("\n")
f.close()
