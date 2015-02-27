
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

if __name__=='__main__':subst('stuff.hbs',
                              {'name': 'Will'},
                              verbose=True)
