#!/usr/bin/env python
from __future__ import print_function
from prelude import *

def xloop(d,doc=None,pfx='',acc=None,
          uri_parms=[],query_parms=[],form_parms=[]):

    if acc is None: acc=[]
    if doc is None: doc=d

    for k,v in d.iteritems():
        if k.startswith('/'):
            new_path = pfx+str(k)

            if type(v)==type({}):
                up = dict(  uri_parms, **v.get(  'uriParameters',{}))
                qp = dict(query_parms, **v.get('queryParameters',{}))
                fp = dict( form_parms, **v.get( 'formParameters',{}))

                def gen_node(v,method):
                    what = v.get(method,{})
                    if not what: return
                    flat_path = (new_path
                                 .replace('/','_').replace('-','_')
                                 .replace('{','_').replace('}','_'))
                    uri  =[dict(v,key_name=k) for k,v in up.iteritems()]
                    query=[dict(v,key_name=k) for k,v in qp.iteritems()]
                    form =[dict(v,key_name=k) for k,v in fp.iteritems()]
                    d=dict(method=method,path=new_path,flat_path=flat_path,
                           parmsx=dict(uri=uri,query=query,form=form))
                    acc.append(d)
                    pass

                if 'type' in v:
                    gen_node(v,'get')
                    gen_node(v,'post')
                    gen_node(v,'delete')
                    pass
                
                xloop(v,doc,pfx=new_path,acc=acc,
                      uri_parms=up,query_parms=qp,form_parms=fp)
                pass
            pass
        pass
    return acc

def gen_yaml_server(document):
    zz = xloop(document)
    from .hb import subst
    subst('__init__.py.hbs',dict(d=zz),outfile='__init__.py')
    subst('__main__.py.hbs',dict(d=zz),outfile='__main__.py')
    subst('use_requests.py.hbs',dict(d=zz),outfile='use_requests.py')
    pass

def main(switch=getarg(1),fname=getarg(2)):
    if switch == '-y':
        global document
        document = load_yaml_document(fname)
        return gen_yaml_server(document)
    elif switch == '-js':
        return usage(1,"I don't know how to deal with a json file yet :(\n")
    usage(1,"bad file type (expected -y or -js)\n")

if __name__=='__main__':main()
