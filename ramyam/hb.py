import os, pybars, collections
from pybars import strlist, Compiler, Scope

def subst(fname,context,verbose=False,outfile=None):
    source = u''+open(fname).read()

    compiler = Compiler()
    template = compiler.compile(source)

    def _recurse(d,doc=None,pfx='',tab='  ',acc=[],uri_paths=[]):
        if doc is None: doc=d
        keylist = ('description','responses','is','body','queryParameters')

        for k,v in d.iteritems():
            path=pfx+str(k)
            new_uri_paths = []
            if type(v)==dict:

                if 'uriParameters' in v:
                    new_uri_paths.append( v['uriParameters'] )
                    pass

                if k.startswith('/'):
                    #print tab, "RECURSP", path, type(v), v.keys()
                    _recurse(v,doc,pfx=path,tab=tab+'  ',acc=acc,uri_paths=uri_paths+new_uri_paths)
                    pass
                elif k in ('get','post','delete'):
                    method=k
                    print tab, "RECURSM", path, type(v), v.keys()
                    print tab, "GENERAT", pfx, method, repr(v)[:200]
                    print tab, '     -----', uri_paths
                    for kk in v:
                        if kk not in keylist:
                            print "OUCH", kk
                            pass
                        pass
                    acc.append( dict(path=pfx,method=method,node=v) )
                    pass
                elif k == 'uriParameters':
                    print tab, "RECURSU", path, type(v), v
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
        
    def _generateFlatTree(this):
        print "GENERATE FLAT TREE", type(this)        
        zz = _recurse(this.root['yaml'])
        from pprint import pprint
        #pprint(zz)
        this.root['d'] = zz
        pass
    
    helpers = {'generateFlatTree':_generateFlatTree}
    output = template(context, helpers=helpers)
    if verbose:
        print(output)
        pass
    if outfile:
        f=open(outfile,'w')
        f.write(''.join(output))
        f.close()
        pass
    return output

import traceback

def mkdir2(dir):
    try:
        os.mkdir(dir)
    except:
        #traceback.print_exc()
        pass

def subst2(zz,fname,infile,language):
    inroot = infile.split('/')[-1]
    if infile.endswith('.hbs'): outfile=infile[:-4]
    inf = 'languages/'+language+'/templates/'+inroot
    #print("S100")
    mkdir2('gen')
    mkdir2('gen/languages')
    mkdir2('gen/languages/'+language)
    mkdir2('gen/languages/'+language+'/'+fname)
    #print("S900")
    dir = 'gen/languages/'+language+'/'+fname
    subst(inf,zz,outfile=dir+'/'+outfile)
    #subst(inf,dict(d=zz),outfile=dir+'/'+outfile)
    pass

if __name__=='__main__':subst('stuff.hbs',
                              {'name': 'Will'},
                              verbose=True)
