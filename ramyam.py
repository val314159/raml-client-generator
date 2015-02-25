#!/usr/bin/env python
from __future__ import print_function
import os, sys, yaml
from pprint import pprint

def getarg(n,m=None):
    try: return sys.argv[n]
    except: return m

def get_paths(doc):
    return (_ for _ in doc.iterkeys() if _.startswith('/'))

def get_resource(doc,typ):
    rct = doc['resourceTypes']
    for rec in rct:
        for k,v in rec.iteritems():
            if k==typ:
                return v
    pass

def gen2(doc,pfx='',parents=[]):
    leftovers = dict(doc)

    leftovers.pop('securitySchemes','')
    leftovers.pop('resourceTypes','')
    leftovers.pop('title','')
    leftovers.pop('traits','')
    docs = leftovers.pop('documentation','')
    if os.environ.get('D'):
        for d in docs:
            print("  '''")
            print(d['title'])
            print('====')
            print(d['content'])
            print("'''")
            pass
        pass
    typ    = leftovers.pop('type','')
    get    = leftovers.pop('get',{})
    post   = leftovers.pop('post',{})
    delete = leftovers.pop('delete',{})
    secBy  = leftovers.pop('securedBy',{})

    uri = leftovers.pop('uriParameters',{})
    urik = ','.join( uri.keys() )
    urik2 = ','+urik if urik else ''

    func_name = pfx.replace('/','_').replace('{','_').replace('}','_').replace('-','_')

    import re
    pfx2 = re.sub('{\w+}','%s',pfx)

    for path in get_paths(doc):
        gen2(doc[path],pfx+path,parents + [uri])
        leftovers.pop(path)
        pass

    rec=None
    method=''
    desc=None

    if get:
        rec=get
        method='get'
    elif post:
        rec=post
        method='post'
    elif delete:
        rec=delete
        method='delete'
        pass

    if rec:
        qp = rec.get('queryParameters',{})
        desc = rec.get('description')

        #################################
        example = ''
        schema = ''
        for k in rec.get('responses',{}).keys():
            v = rec['responses'][k]
            example = ''.join(v.get('body',{}).get('example',''))
            schema  = ''.join(v.get('body',{}).get('schema',''))
            if example: example = 'Example: '+example
            if schema : schema  = 'Schema : '+schema
            pass

        #################################
        if uri:
            print('#uri',repr(uri)[:200])
            print('#urip',repr(parents)[:200])
            pass

        xexample,xschema='',''

        if os.environ.get('E'):
            xexample=example
            pass
        if os.environ.get('S'):
            xschema=schema
            pass

        d = dict(pfx=pfx, pfx2=pfx2,
                 desc=desc, method=method, func_name=func_name,
                 example=example, schema=schema,
                 xexample=xexample, xschema=xschema,
                 urik=str(urik), urik2=str(urik2))

        print('''\
  def f{func_name}_{method}(_{urik2}):
    """{desc}{xexample}{xschema}"""
    url = '{pfx2}' % ({urik})
    ret = requests.{method}(url)
    return ret\
'''.format(**d))

    pass

def main(fname=getarg(1)):
    global document
    document = yaml.load(open(fname))
    print("#ramyam 1", fname)
    print("import requests")
    print("class API:")
    gen2(document)
    print()
    print("api = API()")
    pass
if __name__=='__main__': main()
