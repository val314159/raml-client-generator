from __future__ import print_function
import os, sys, yaml, re
from pprint import pprint,pformat
from cgi import parse_qs, escape

def getarg(n,m=None):
    try: return sys.argv[n]
    except: return m

def usage(code,msg):
    sys.stderr.write(msg)
    sys.exit(code)
    pass

def load_yaml_document(fname):
    from yaml_loader import Loader
    full_name = os.environ.get('INDIR','.')+'/'+fname
    document = yaml.load(open(full_name),Loader)
    return document

access_token='185651424.1fb234f.713bd9c785c444ce8d99e4032a55cfa4'
def set_access_token(at): global access_token ; access_token=at
def get_access_token():   return access_token
