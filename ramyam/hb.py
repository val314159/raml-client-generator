import os

def subst(fname,context,verbose=False,outfile=None):
    import pybars

    source = u''+open(fname).read()

    compiler = pybars.Compiler()
    template = compiler.compile(source)

    def _bold(this, name):
        return pybars.strlist(['<strong>', name, '</strong>'])
    helpers = {'bold': _bold}

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
