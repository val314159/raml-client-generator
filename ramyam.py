import os, sys, yaml; from pprint import pprint

if __name__=='__main__':
    fname=sys.argv[1]
    print "ramyam 1", fname
    x = yaml.load(open(fname))
    #pprint(x)
    for k1,v1 in x.iteritems():
        if k1=='resourceTypes':
            print '1!', k1
            pprint(v1)
        elif not k1.startswith('/') or k1=='resourceTypes':
            print '1-', k1
            pass
        else:
            print '1=', k1, v1.get('type'), v1.keys()
            for k2,v2 in v1.iteritems():
                if not k2.startswith('/'):
                    #print '2---', k2
                    pass
                else:
                    print '2===', k2, v2.get('type'), v2.keys()
                    for k3,v3 in v2.iteritems():
                        if not k3.startswith('/'):
                            #print '3-----', k3
                            pass
                        else:
                            print '3=====', k3, v3.get('type'), v3.keys()
                            for k4,v4 in v3.iteritems():
                                if not k4.startswith('/'):
                                    #print '4-------', k4
                                    pass
                                else:
                                    print '4=======', k4, v4.get('type'), v4.keys()
                                    print '4======= . . . ', v4.keys()
                                    pass
                                pass
                            pass
                        pass
                    pass
                pass
            pass
        pass
    pass

