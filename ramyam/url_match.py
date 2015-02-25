#!/usr/bin/env python
from __future__ import print_function
import os, sys, yaml, re
from pprint import pprint,pformat

def getarg(n,m=None):
    try: return sys.argv[n]
    except: return m

def convert_url(x):
    return x.replace('{','(?P<').replace('}','>\w+)')

def match_url(pat1,s):
    m = re.match(pat1,s)
    if m:
        return m.group

def match_first(arr,url):
    for pat,fn in arr:
        m = match_url(pat,url)
        if m: return fn(m)
        pass

if __name__=='__main__':
    pat1=convert_url(r'/base/{xxx}/{yyy}')
    pat2=convert_url(r'/base/{xxx}/{yyy}/whatevz')

    def do_pat1(m):
        print("DO IT1", m)
        return m

    def do_pat2(m):
        print("DO IT2", m)
        return m

    arr = [(pat1,do_pat1),
           (pat2,do_pat2)]
    x = match_first(arr,'/qqqqq')
    print(x)
    x = match_first(arr,'/base/xrx/yy/whatevz')
    print(x,x('xxx'))
    x = match_first(arr,'/base/xx/yeey')
    print(x,x('xxx'))
    pass
