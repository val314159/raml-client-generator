import os, pybars, collections
from pybars import strlist, Compiler, Scope

def _transmogrify_params(parms):
    arr = []
    for parm in parms:
        for k1,v1 in parm.iteritems():
            arr.append( dict(v1, key_name=k1) )
            pass
        pass
    return arr

def flattenMethodName(this, methodName):
    print "HOW DO I DO THIS?  (flatten a method name)"
    pass

def _recurse(node,doc=None,pfx='',tab='  ',acc=[],uri_parms=[]):
    if doc is None: doc=node
    keylist = ('description','responses','is','body','queryParameters')

    for k,v in node.iteritems():
        path=pfx+str(k)
        new_uri_parms = []
        if type(v)==dict:

            if 'uriParameters' in v:
                new_uri_parms.append( v['uriParameters'] )
                pass

            if k.startswith('/'):
                _recurse(v,doc,pfx=path,tab=tab+'  ',acc=acc,uri_parms=uri_parms+new_uri_parms)
                pass

            elif k in ('get','post','delete'):
                method=k
                for kk in v:
                    if kk not in keylist:
                        print "OUCH", kk
                        pass
                    pass

                record = dict(path=pfx,method=method,keys=v.keys(),parmsx={})

                zuri_parms=uri_parms+new_uri_parms
                if zuri_parms:
                    record['uriParameters'] = _transmogrify_params(zuri_parms)
                    record['parmsx']['uri'] = _transmogrify_params(zuri_parms)
                    pass

                if 'queryParameters' in v:
                    record['queryParameters'] =_transmogrify_params([v['queryParameters']])
                    record['parmsx']['query'] =_transmogrify_params([v['queryParameters']])
                    pass

                if 'body' in v:
                    for kk,vv in v.get('body').iteritems():
                        typ = ''
                        if kk=='formParameters':
                            record['formParameters'] = _transmogrify_params([vv])
                            record['parmsx']['form'] = _transmogrify_params([vv])
                            pass
                        elif type(vv)==dict:
                            for kkk,vvv in vv.iteritems():
                                if kkk=='formParameters':
                                    record['formParameters'] = _transmogrify_params([vvv])
                                    record['paramsx','form'] = _transmogrify_params([vvv])
                                    pass
                                else:
                                    print "k3 v3", kkk, vvv
                                    pass
                                pass
                            pass
                        pass
                    pass

                acc.append( record )
                pass
            elif k == 'uriParameters':
                #print tab, "RECURSU", path, type(v), v
                pass
            else:
                print tab, "RECURSI", path, type(v), v.keys()
                pass
            pass
        elif type(v)==str:
            #print tab, "RECURSS", path, type(v), repr(v)[:200]
            pass
        else:
            #print tab, "RECURSE", path, type(v)
            pass
        pass
    return acc

def generateFlatTree(this):
    print "GENERATE FLAT TREE", type(this)
    zz = _recurse(this.root['yaml'])
    from pprint import pprint
    print
    print'-'*80
    print
    pprint(zz)
    this.root['d'] = zz
    pass
 
