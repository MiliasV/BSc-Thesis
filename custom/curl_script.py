#!/usr/bin/python
import os,sys
"os.system(curl -w @for_curl.txt -o /dev/null -s, sys.argv[0].IP())"

for i in range(1000):
        #cmd= "curl " + sys.argv[1] +" >> outputcurl.txt"
        cmd= "curl " + sys.argv[1] +" >> outputcurl.txt"
        os.system(cmd)

