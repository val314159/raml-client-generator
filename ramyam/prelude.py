from __future__ import print_function
import os, sys, yaml, re
from pprint import pprint,pformat

def getarg(n,m=None):
    try: return sys.argv[n]
    except: return m

def usage(code,msg):
    sys.stderr.write(msg)
    sys.exit(code)
    pass

def load_yaml_document(fname):
    from yaml_loader import Loader
    document = yaml.load(open(fname),Loader)
    return document
