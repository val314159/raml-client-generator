#!/usr/bin/env python
import os, sys, yaml
from pprint import pprint

def getarg(n,m=None):
    try: return sys.argv[n]
    except: return m

def get_paths(doc):
    return (_ for _ in doc.iterkeys() if _.startswith('/'))

def get_nonpaths(doc):
    return (_ for _ in doc.iterkeys() if not _.startswith('/'))

def get_resource(doc,typ):
    rct = doc['resourceTypes']
    for rec in rct:
        for k,v in rec.iteritems():
            if k==typ:
                return v
    pass

def gen2(doc,pfx=''):
    p = list(get_paths(doc))
    np= list(get_nonpaths(doc))
    print '**** %40s %120s %120s' % (repr(pfx), str(p), str(np))
    leftovers = dict(doc)
    for path in get_paths(doc):
        #print "== PATH", pfx, path, [_ for _ in doc[path].keys()]
        #typ = doc[path].get('type')
        #if typ:
        #    print "#ITS A TYP", repr(typ), pfx+path

        gen2(doc[path],pfx+path)
        leftovers.pop(path)
        pass

    typ    = leftovers.pop('type','')
    get    = leftovers.pop('get','')
    post   = leftovers.pop('post','')
    delete = leftovers.pop('delete','')
    leftovers.pop('securedBy','')

    uri = leftovers.pop('uriParameters',{})
    urik = ','.join( uri.keys() )
    func_name = pfx.replace('/','_').replace('{','_').replace('}','_')

    if get:
        print 'get',repr(get)[:200]
        print '''
  def {func_name}_{method}(_,{urik}):
    url = '{pfx}' % ({urik})
    ret = requests.{method}(url)
    return ret
'''.format(pfx=pfx,method='get',func_name=func_name,urik=str(urik))
        pass
    if post:
        print 'post',repr(post)[:200]
        print '''
  def {func_name}_{method}(_,{urik}):
    url = '{pfx}' % ({urik})
    ret = requests.{method}(url)
    return ret
'''.format(pfx=pfx,method='post',func_name=func_name,urik=str(urik))
        pass
    if delete:
        print 'delete',repr(delete)[:200]
        print '''
  def {func_name}_{method}(_,{urik}):
    url = '{pfx}' % ({urik})
    ret = requests.{method}(url)
    return ret
'''.format(pfx=pfx,method='delete',func_name=func_name,urik=str(urik))
        pass
    if uri:
        print 'uri',repr(uri)[:200]
        pass
    #print uri

    leftovers.pop('securitySchemes','')
    leftovers.pop('resourceTypes','')
    leftovers.pop('title','')
    leftovers.pop('traits','')
    leftovers.pop('documentation','')
    
    print "LEFTOVERS", repr(leftovers)[:200]
    pass

def gen1(doc):
    print doc.keys()
    for path in get_paths(doc):
        print "== PATH", path
        typ = doc[path].get('type')
        if typ:
            print "ITS A TYP", typ
            rc = get_resource(doc,typ)
            print "RC =", rc.keys()
            for k,v in rc.iteritems():
                print '. . . . . .', k
                pprint(v.get('queryParameters'))
                pass            
            #pprint(rc)
        else:
            pass

    pass

def main(fname=getarg(1)):
    print "#ramyam 1", fname
    global document
    document = yaml.load(open(fname))
    print "import requests"
    gen2(document)
    print
    print "api = API()"
    pass
if __name__=='__main__': main()
