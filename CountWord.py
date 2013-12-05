#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import ConfigParser
import argparse

import pystardict



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

        print "Dictionary is %s"%(dict_data)  

        print "Start checking dictionary...please wait\n"
        #for (k,c) in d.items():
        for i in sort:
            f.write("\n\n"+i[0]+" "+str(i[1])+"\n")
            searchword=i[0]
            try:
              f.write(str(pydict[searchword])) 
            except Exception, e:
                f.write(searchword+" not found in this dict.")
                # try:
                #     searchword="".join(difflib.get_close_matches(i[0],pylist)[0])
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
 