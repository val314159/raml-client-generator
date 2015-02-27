#!/usr/bin/env python
from __future__ import print_function
from prelude import *

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
        pfx3 = pfx.replace('{','P<').replace('}','>')
        d = dict(pfx=pfx, pfx2=pfx2, baseUri=baseUri,
                 pfx3=pfx3,
                 access_token=access_token,
                 desc=desc, method=method, func_name=func_name,
                 example=example, schema=schema,
                 xexample=xexample, xschema=xschema,
                 urik=str(urik), urik2=str(urik2))

        print('''\
  def svr{func_name}_{method}(_,env,start):
    print("ENV", env)
    query_string = env['QUERY_STRING']
    print("QUERY_STRING", query_string)
    path_info = env['PATH_INFO']
    print("PATH_INFO", path_info)
    d = parse_qs(query_string)
    pfx3 = '{pfx3}'
    print("PFX3", pfx3)
    #url = '{baseUri}{pfx2}' % ({urik})
    #ret = requests.{method}(url,verify=False)
    return _.clt{func_name}_{method}(_{urik2})
  def clt{func_name}_{method}(_{urik2}):
    """{desc}{xexample}{xschema}    """
    url = '{baseUri}{pfx2}' % ({urik})
    ret = requests.{method}(url,verify=False)
    params=dict(access_token='{access_token}')
    ret = requests.{method}(url,params=params,verify=False)
    return ret\
'''.format(**d))
    pass

def xloop(d,doc=None,pfx='',
          uri_parms=[],query_parms=[],form_parms=[],
          tab='--> '):

    def xonce_path(k,v):
        print(tab+'+ k =',k,'URI_PARMS =',uri_parms)
        if type(v)==type(''):
            print(tab+'|STR TYPE ' + repr(v))
            pass
        elif type(v)==type({}):
            print(tab+'|DIC TYPE, keys =' + repr(v.keys()))

            #if 'uriParameters' in v:
            x = v.get('uriParameters',{})
            print(tab+"|hasUriParms:" + repr(x))

            up = dict(uri_parms,  **v.get('uriParameters',{}))
            qp = dict(query_parms,**v.get('queryParameters',{}))
            fp = dict(form_parms, **v.get('formParameters',{}))

            xloop(v,doc,pfx=pfx+str(k),
                  uri_parms=up,query_parms=qp,form_parms=fp,
                  tab=tab+'  ')

            pass
        else:
            print(tab+'|UNKNOWN TYPE ' + str(type(v)))
            pass
        pass

    if doc is None: doc=d
    #print("def xloop",repr((d.keys(),repr(pfx),uri_parms,query_parms,form_parms)))
    for k,v in d.iteritems():
        if k.startswith('/'):
            xonce_path(k,v)


def loop(d,doc,pfx='',uri_parms=[],query_parms=[],form_parms=[]):
    for k,v in d.iteritems():
        if not k.startswith('/'):
            continue
        print(' - ', pfx+str(k))
        if type(v)==type([]):
            print(tab+"LIST:")
            #pprint(v)
            pass
        elif v in [True,False]:
            print(tab+"BOOL:")
            #pprint(v)
            pass
        elif type(v)==type(0):
            print(tab+"INT:")
            #pprint(v)
            pass
        elif type(v)==type(''):
            print(tab+"STR:")
            pprint(v[:80])
            pass
        elif type(v)==type({}):
            print(tab+"DICT:")
            #print(" ..k..",v.keys())
            if 'uriParameters' in v:
                print('uriParameters',v['uriParameters'])
                pass
            if 'queryParameters' in v:
                print('queryParameters',v['queryParameters'])
                pass
            if 'formParameters' in v:
                print('formParameters',v['formParameters'])
                pass
            #new_path = pfx+str(k)
            #loop(v,doc,new_path,uri_parms,query_parms,form_parms)
        else:
            print('UNKNOWN TYPE ' + str(type(v)))
            pass
        pass
    pass

def gen_yaml_server2(document):
    print('###')
    xloop(document,tab='@@@@ ')
    print('###')
    pass

def gen_yaml_server(document):
    print("#", [_ for _ in document.keys() if not _.startswith('/')])
    print("import requests")
    print("from urlparse import parse_qs")
    print("class RamlObj:")
    print("  traits = " + pformat(document.get('traits',{})))
    print("  securitySchemes = " + pformat(document.get('securitySchemes',{})))
    print("  resourceTypes = " + pformat(document.get('resourceTypes',{})))
    #print("  securedBy =", repr(document['securedBy']))
    print("  mediaType =", repr(document.get('mediaType','')))
    print("  baseUri =", repr(document.get('baseUri','')))
    print("  version =", repr(document.get('version','')))
    print("  paths =", repr([k for k in document.keys() if k.startswith('/')]))
    gen0(document)
    print("")
    print("if __name__=='__main__':")
    print("  import ramyam.wsgi_svr")
    print("  ramyam.wsgi_svr.main(RamlObj)")
    pass

def main(switch=getarg(1),fname=getarg(2)):
    print("#ramyam server from", switch, fname)
    if switch == '-y':
        global document
        document = load_yaml_document(fname)
        return gen_yaml_server2(document)
    elif switch == '-js':
        return usage(1,"I don't know how to deal with a json file yet :(\n")
    usage(1,"bad file type (expected -y or -js)\n")

if __name__=='__main__':main()
