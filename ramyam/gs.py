#!/usr/bin/env python
from __future__ import print_function
from prelude import *

def xprint(*a,**kw):
    #print(*a,**kw)
    pass

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
            xprint("  '''")
            xprint("#", title)
            xprint(d['title'])
            xprint('====')
            xprint(d['content'])
            xprint("'''")
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
            #xprint('#uri',repr(uri)[:200])
            #xprint('#urip',repr(parents)[:200])
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

        xprint('''\
  def svr{func_name}_{method}(_,env,start):
    xprint("ENV", env)
    query_string = env['QUERY_STRING']
    xprint("QUERY_STRING", query_string)
    path_info = env['PATH_INFO']
    xprint("PATH_INFO", path_info)
    d = parse_qs(query_string)
    pfx3 = '{pfx3}'
    xprint("PFX3", pfx3)
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
          tab='--> ',acc=None):
    if acc is None: acc=[]

    def xonce_path(k,v):
        new_path = pfx+str(k)

        xprint(tab+'+ k =',k,'URI_PARMS =',uri_parms)
        if type(v)==type(''):
            xprint(tab+'|STR TYPE ' + repr(v))
            pass
        elif type(v)==type({}):
            xprint(tab+'|DIC TYPE, keys =' + repr(v.keys()))

            #if 'uriParameters' in v:
            x = v.get('uriParameters',{})
            xprint(tab+"|hasUriParms:" + repr(x))

            up = dict(uri_parms,  **v.get('uriParameters',{}))
            qp = dict(query_parms,**v.get('queryParameters',{}))
            fp = dict(form_parms, **v.get('formParameters',{}))

            if 'type' in v:
                xprint(tab+'// GENERATE NODE ', v['type'], up, qp, fp)
                g=v.get('get',{})
                p=v.get('post',{})
                d=v.get('delete',{})
                xprint(tab+'||--- METHOD get    ' + str(g.keys()))
                xprint(tab+'||--- METHOD post   ' + str(p.keys()))
                xprint(tab+'||--- METHOD delete ' + str(d.keys()))

                def gen_node(method,what):
                    #print(".gen ", method,new_path,up,qp,fp)
                    acc.append((method,new_path,dict(uri=up,query=qp,form=fp)))
                    pass

                if g: gen_node('get',g)
                if p: gen_node('post',p)
                if d: gen_node('delete',d)

                xprint(tab+'\\\\ GENERATE NODE', new_path)
                pass

            xloop(v,doc,pfx=new_path,tab=tab+'  ',
                  uri_parms=up,query_parms=qp,form_parms=fp,acc=acc)
            
            pass
        else:
            xprint(tab+'|UNKNOWN TYPE ' + str(type(v)))
            pass
        pass

    if doc is None: doc=d
    #xprint("def xloop",repr((d.keys(),repr(pfx),uri_parms,query_parms,form_parms)))
    for k,v in d.iteritems():
        if k.startswith('/'):
            xonce_path(k,v)
    return acc

def loop(d,doc,pfx='',uri_parms=[],query_parms=[],form_parms=[]):
    for k,v in d.iteritems():
        if not k.startswith('/'):
            continue
        xprint(' - ', pfx+str(k))
        if type(v)==type([]):
            xprint(tab+"LIST:")
            #pxprint(v)
            pass
        elif v in [True,False]:
            xprint(tab+"BOOL:")
            #pxprint(v)
            pass
        elif type(v)==type(0):
            xprint(tab+"INT:")
            #pxprint(v)
            pass
        elif type(v)==type(''):
            xprint(tab+"STR:")
            pxprint(v[:80])
            pass
        elif type(v)==type({}):
            xprint(tab+"DICT:")
            #xprint(" ..k..",v.keys())
            if 'uriParameters' in v:
                xprint('uriParameters',v['uriParameters'])
                pass
            if 'queryParameters' in v:
                xprint('queryParameters',v['queryParameters'])
                pass
            if 'formParameters' in v:
                xprint('formParameters',v['formParameters'])
                pass
            #new_path = pfx+str(k)
            #loop(v,doc,new_path,uri_parms,query_parms,form_parms)
        else:
            xprint('UNKNOWN TYPE ' + str(type(v)))
            pass
        pass
    pass

def gen_yaml_server2(document):
    xprint('###')
    zz = xloop(document,tab='@@@@ ')
    xprint('###')
    pprint(zz)
    pass

def gen_yaml_server(document):
    xprint("#", [_ for _ in document.keys() if not _.startswith('/')])
    xprint("import requests")
    xprint("from urlparse import parse_qs")
    xprint("class RamlObj:")
    xprint("  traits = " + pformat(document.get('traits',{})))
    xprint("  securitySchemes = " + pformat(document.get('securitySchemes',{})))
    xprint("  resourceTypes = " + pformat(document.get('resourceTypes',{})))
    #xprint("  securedBy =", repr(document['securedBy']))
    xprint("  mediaType =", repr(document.get('mediaType','')))
    xprint("  baseUri =", repr(document.get('baseUri','')))
    xprint("  version =", repr(document.get('version','')))
    xprint("  paths =", repr([k for k in document.keys() if k.startswith('/')]))
    gen0(document)
    xprint("")
    xprint("if __name__=='__main__':")
    xprint("  import ramyam.wsgi_svr")
    xprint("  ramyam.wsgi_svr.main(RamlObj)")
    pass

def main(switch=getarg(1),fname=getarg(2)):
    xprint("#ramyam server from", switch, fname)
    if switch == '-y':
        global document
        document = load_yaml_document(fname)
        return gen_yaml_server2(document)
    elif switch == '-js':
        return usage(1,"I don't know how to deal with a json file yet :(\n")
    usage(1,"bad file type (expected -y or -js)\n")

if __name__=='__main__':main()
