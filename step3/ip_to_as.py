#/usr/bin/python  
import time
import re
import os
import sys
import json
import pyasn
import pandas as pd
import numpy as np
import itertools
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from pprint import pprint
import metis
#Author: Vasileios Milias


def ip_as_mapping(ip_attack_file,ip_asdata):
    #input1 : file with requested ips
    #input2 : file that contains data for ip-as mapping
   
    asndb=pyasn.pyasn(ip_asdata)
    df=pd.read_csv(ip_attack_file,header=None,usecols=[2],delimiter=" ")
    l=df.drop_duplicates().values.tolist()
    for i in l:
        for ip in i:
            ip='.'.join(ip.split('.')[0:4])
            print ip         
            print asndb.lookup(ip)

if __name__=='__main__':
    #input2 : number of Vms (=> list of Vms with credentials)
    start_time=time.time()
    ip_as_mapping(sys.argv[1],sys.argv[2])
    print time.time()-start_time
