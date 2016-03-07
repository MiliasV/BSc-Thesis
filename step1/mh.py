#/usr/bin/python  
import time
import os
import sys
import pyasn
from ast import literal_eval
#Author: Vasileios Milias

def ases(file):
    #input1 : file with lines in format
    #         ip
    #         (as,ip)
    #returns : list with ases of attack 
    l=[]
    fp=open(file)
    for i, line in enumerate(fp):
        if i%2==1:
            l.append(line)
    return l
    #victim's as
    #print asndb.lookup('71.126.22.64')

if __name__=='__main__':
    #start_time=time.time()
    aS=[]
    k=ases(sys.argv[1])
    for l in k:
        aS.append(literal_eval(l)[0])
    aS=list(set(aS))
    for i in aS:
        print i
    #print time.time()-start_time
