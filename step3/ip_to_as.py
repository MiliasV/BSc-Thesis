#/usr/bin/python  
import time
import os
import sys
import pyasn
import pandas as pd
import numpy as np
import networkx as nx

#Author: Vasileios Milias

def ip_as_mapping(ip_attack_file,ip_asdata):
    #input1 : file with requested ips (file of attack)
    #input2 : file that contains data for ip-as mapping
    #output : ip-as match 
    asndb=pyasn.pyasn(ip_asdata)
    df=pd.read_csv(ip_attack_file,header=None,usecols=[2],delimiter=" ")
    l=df.drop_duplicates().values.tolist()
    for i in l:
        for ip in i:
            ip='.'.join(ip.split('.')[0:4])
            print ip         
            print asndb.lookup(ip)
    #victim's as
    #print asndb.lookup('71.126.22.64')

if __name__=='__main__':
    start_time=time.time()
    ip_as_mapping(sys.argv[1],sys.argv[2])
    print time.time()-start_time
