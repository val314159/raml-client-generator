#!/usr/bin/env python
from __future__ import print_function
from prelude import *

import datetime
#dthandler = lambda obj: (
#    obj.isoformat()
#    if isinstance(obj, datetime.datetime)
#    or isinstance(obj, datetime.date)
#    else None)
#>>> json.dumps(datetime.datetime.now(), default=dthandler)
#'"2010-04-20T20:08:21.634121"'

# ISO 8601 format.
def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    #elif isinstance(obj, ...):
    #    return ...
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

def xloop(d,doc=None,pfx='',acc=None,
          uri_parms=[],query_parms=[],form_parms=[]):
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

                    qp = what.get('queryParameters',{})
                    body = what.get('body',{})
                    nnfp = {}
                    if body:
                        kk,vv = list(body.iteritems())[0]
                        if kk == 'formParameters':
                            nnfp = vv
                            pass
                        elif kk == 'application/x-www-form-urlencoded':
                            nnfp = vv.get('formParameters',{})
                            pass
                        else:
                            print("#Unknown ",kk)
                            pass
                        #print("#NFP", nnfp)
                        pass
                    uri  =[dict(v,key_name=k) for k,v in up.iteritems()]
                    query=[dict(v,key_name=k) for k,v in qp.iteritems()]
                    form =[dict(v,key_name=k) for k,v in (nnfp or fp).iteritems()]
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
    return dict(d=acc)

def gen_yaml_server(zz,fname):
    from .hb import subst2

    # python
    subst2(zz,fname,'__init__.py.hbs',    'python')
    subst2(zz,fname,'__main__.py.hbs',    'python')
    subst2(zz,fname,'use_requests.py.hbs','python')
    # C
    subst2(zz,fname,'c_curl.c.hbs','c')
    pass

def main(switch=getarg(1),fname=getarg(2)):
    if switch == '-y':
        global document
        print("QQZ")
        print("QQZ FNAME", fname)
        document = load_yaml_document(fname)
        zz = dict(yaml=document)
        if '-intermediate' in sys.argv:
            print(json.dumps(zz,indent=4,default=handler))
            return
        else:
            return gen_yaml_server(zz,fname)
        pass
    elif switch == '-js':
        return usage(1,"I don't know how to deal with a json file yet :(\n")
    usage(1,"bad file type (expected -y or -js)\n")

if __name__=='__main__':main()
