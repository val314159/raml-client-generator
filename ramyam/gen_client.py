#!/usr/bin/env python
from __future__ import print_function
from prelude import *

access_token='185651424.1fb234f.713bd9c785c444ce8d99e4032a55cfa4'

def get_paths(doc):
    return (_ for _ in doc.iterkeys() if _.startswith('/'))

def get_resource(doc,typ):
    rct = doc['resourceTypes']
    for rec in rct:
        for k,v in rec.iteritems():
            if k==typ:
                return v
    pass

def gen0(doc):
    leftovers = dict(doc)
    docs = leftovers.pop('documentation','')
    title   = leftovers.pop('title','')
    version = str(leftovers.pop('version',''))
    baseUri = leftovers.pop('baseUri','')
    baseUri = baseUri.replace('{version}',version)
    if baseUri.endswith('/'):
        baseUri = baseUri[:-1]
        pass
    if os.environ.get('D'):
        for d in docs:
            print("  '''")
            print("#", title)
            print(d['title'])
            print('====')
            print(d['content'])
            print("'''")
            pass
        pass
    ret = gen2(baseUri,leftovers,'',[])
    return ret

def gen2(baseUri,doc,pfx,parents):
    leftovers = dict(doc)

    leftovers.pop('securitySchemes',{})
    leftovers.pop('resourceTypes',{})
    leftovers.pop('title','')
    leftovers.pop('traits',{})

    typ    = leftovers.pop('type','')
    get    = leftovers.pop('get',{})
    post   = leftovers.pop('post',{})
    delete = leftovers.pop('delete',{})
    secBy  = leftovers.pop('securedBy',{})

    uri = leftovers.pop('uriParameters',{})
    arr = []
    for p in parents:
        for k,v in p.iteritems():
            arr.append((k,v))
            pass
    for k,v in uri.iteritems():
        arr.append((k,v))
        pass
    urik = ','.join( k for k,v in arr )
    urik2 = ','+urik if urik else ''

    func_name = pfx.replace('/','_').replace('{','_').replace('}','_').replace('-','_').replace('.','_')

    pfx2 = re.sub('{\w+}','%s',pfx)

    for path in get_paths(doc):
        gen2(baseUri,doc[path],pfx+path,parents + [uri])
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
            #print('#uri',repr(uri)[:200])
            #print('#urip',repr(parents)[:200])
            pass
        xexample,xschema='',''
        if os.environ.get('E'):
            xexample=example
            pass
        if os.environ.get('S'):
            xschema=schema
            pass

        d = dict(pfx=pfx, pfx2=pfx2, baseUri=baseUri,
                 access_token=access_token,
                 desc=desc, method=method, func_name=func_name,
                 example=example, schema=schema,
                 xexample=xexample, xschema=xschema,
                 urik=str(urik), urik2=str(urik2))

        print('''\
  def rpc{func_name}_{method}(_{urik2}):
    """{desc}{xexample}{xschema}    """
    url = '{baseUri}{pfx2}?access_token={access_token}' % ({urik})
    ret = requests.{method}(url,verify=False)
    return ret\
'''.format(**d))
    pass

def gen_yaml_client(document):
    print("#", [_ for _ in document.keys() if not _.startswith('/')])
    print("import requests")
    print("class API:")
    print("  access_token = " + repr(access_token))
    print("  traits = " + pformat(document.get('traits',{})))
    print("  securitySchemes = " + pformat(document.get('securitySchemes',{})))
    print("  resourceTypes = " + pformat(document.get('resourceTypes',{})))
    #print("  securedBy =", repr(document['securedBy']))
    print("  mediaType =", repr(document.get('mediaType','')))
    print("  baseUri =", repr(document.get('baseUri','')))
    print("  version =", repr(document.get('version','')))
    print("  paths =", repr([k for k in document.keys() if k.startswith('/')]))
    gen0(document)
    print()
    print("api = API()")
    pass

def main(switch=getarg(1),fname=getarg(2)):
    print("#ramyam client from", switch, fname)
    if switch == '-y':
        global document
        document = load_yaml_document(fname)
        return gen_yaml_client(document)
    elif switch == '-js':
        return usage(1,"I don't know how to deal with a json file yet :(\n")
    usage(1,"bad file type (expected -y or -js)\n")

if __name__=='__main__':main()
