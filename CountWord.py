#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import ConfigParser
import argparse
import difflib 
from stemming.porter2 import stem
from stemming.lovins import stem as stem2
from nltk.stem.wordnet import WordNetLemmatizer
import pystardict


def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = []

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    n = len(word)
    return set([word[0:i]+word[i+1:] for i in range(n)] +                     # deletion
               [word[0:i]+word[i+1]+word[i]+word[i+2:] for i in range(n-1)] + # transposition
               [word[0:i]+c+word[i+1:] for i in range(n) for c in alphabet] + # alteration
               [word[0:i]+c+word[i:] for i in range(n+1) for c in alphabet])  # insertion

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return candidates



def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="plot filename", nargs='?')
    args = parser.parse_args()

    filename = None
    directory = None
    if args.file != None:
        directory, filename = os.path.split(args.file)

    return directory, filename


def WhiteWord():
    import re
    f=open("wordlist.txt")
    txt=f.read()
    f.close()
    d={}
    s=[0]
    def handle(m):
            w=m.group(0)
            w=w.lower()
            d[w]=d.get(w,0)+1
            s[0]+=1

    txt=re.compile(r'\b[a-zA-Z]+\b').sub(handle,txt)
    return d

def WordCount(file):   
    #file=raw_input("Enter source file:\n")
    from time import clock
    start=clock()
    import re
    f=open(file)
    txt=f.read()
    f.close()
    d={}
    s=[0]
    def handle(m):
            w=m.group(0)
            w=w.lower()
            d[w]=d.get(w,0)+1
            s[0]+=1

    txt=re.compile(r'\b[a-zA-Z]+\b').sub(handle,txt)
    #print sorted(d.items(),key=lambda d:d[1])[-10:]

    #print 'There are %d words in %s'%(s[0],file)
    print 'There are %d words in %s'%(len(d),file)
    finsih=clock()
    #print 'Run time is %d s'%(finsih - start)
    return d


def longRunning(allfilename):
        if allfilename==None:
            print "Please open a text file first."
            return;
        lmtzr = WordNetLemmatizer()
        f=open(allfilename+"_out.txt","w")
        print "Output file will be %s"%(allfilename+"_out.txt")
        d=WordCount(allfilename)
        w=WhiteWord().keys()
        print "Remove white word from list ..."
        for wo in w:
            d.pop(wo,None)
        sort=sorted(d.items(),key=lambda d:d[1],reverse=True)
        print "Word sorted and distincted\n"

        config = ConfigParser.RawConfigParser()
        config.read('dict.ini')
        
        dict_type = config.get('dict', 'type')
        dict_data = config.get('dict', 'dict')
        pydict=pystardict.Dictionary(dict_data+"\\"+dict_data)        
        pylist=pydict.keys()


        # 
        #     print i[0]
        #     correct(i[0]) 
        # print "Start get the matched word "
        # for i in sort:
        #     try:
        #         if i[0] not in pylist:
        #             searchword1="".join(difflib.get_close_matches(i[0],pylist)[0])
        #         # d.pop(i[0]) 
        #         print i[0]
        #         print searchword1
        #         # f.write("Maybe "+searchword+"?\n")
        #                 #"".join(searchword)                    
        #         # f.write(str(pydict[searchword]))     
        #     except Exception, e:
        #                 # f.write("Really not found.\n")
        #                 pass
        

        print "Dictionary is %s"%(dict_data)  

        print "Start checking dictionary...please wait\n"
        #for (k,c) in d.items():
        def writeword(searchword):
            if searchword in pylist:
                f.write(str(pydict[searchword]))

        for i in sort:
            f.write("\n\n"+i[0]+" "+str(i[1])+"\n")
            searchword=i[0]
            if i[0] in pylist:
                # f.write("\n\n"+i[0]+" "+str(i[1])+"\n")
                f.write(str(pydict[searchword]))
            else:
                # searchword=lmtzr.lemmatize(i[0])
                # if searchword in pylist:
                #     f.write(str(pydict[searchword]))
                #     continue
                try:
                    searchword=stem(i[0])
                    writeword(searchword)
                    searchword=stem2(i[0])
                    writeword(searchword)
               
                    searchword=difflib.get_close_matches(i[0],pylist)[0]
                    writeword(searchword)
                except Exception, e:
                    pass
                
                


            # try:
            #     f.write(str(pydict[searchword])) 
            # except Exception, e:
            #     try:
            #         searchword=lmtzr.lemmatize(i[0])
            #         f.write(str(pydict[searchword]))
            #     except Exception, e:
            #         f.write(searchword+" not found in this dict.")
            #     # try:
                #     searchword=difflib.get_close_matches(i[0],pylist)[0]
                #     f.write("Maybe "+searchword+"?\n")
                #     #"".join(searchword)                    
                #     f.write(str(pydict[searchword]))     
                # except Exception, e:
                #     f.write("Really not found.\n")
        print "Finished"
        f.close()



if __name__ == '__main__':
    
    file=raw_input("Enter source file:\n")
    longRunning(file)
    # app = wx.App(False)
    # frame = FrameMain("CountWord")
    # app.frame=frame
    # directory, filename = arguments()

    # if filename != None:
    #     frame.open(directory, filename)
    # sys.stdout = SysOutListener()
    # app.MainLoop()
 