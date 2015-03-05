#!/usr/bin/env python
from __future__ import print_function
from prelude import *
from .hb import subst2

def handler(obj):
    if not hasattr(obj, 'isoformat'):
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))
	return obj.isoformat()

def main(switch=getarg(1),fname=getarg(2)):
    if switch == '-y':
        global document
        yaml = load_yaml_document(fname)
        document = dict(yaml=yaml)
        if '-intermediate' in sys.argv:
            print(json.dumps(document,indent=4,default=handler))
            return            
        else:
            # python
            subst2(document,fname,'__init__.py.hbs',    'python')
            subst2(document,fname,'__main__.py.hbs',    'python')
            subst2(document,fname,'use_requests.py.hbs','python')
            # C
            subst2(document,fname,'c_curl.c.hbs','c')
            return
        pass
    elif switch == '-js':
        return usage(1,"I don't know how to deal with a json file yet :(\n")
    usage(1,"bad file type (expected -y or -js)\n")

if __name__=='__main__':main()
