from __future__ import print_function

def wrap(attr,env,start):
    print("QQQQQQ 1", repr(attr))
    print("QQQQQQ 2", repr(env))
    print("QQQQQQ 3", repr(start))
    for chunk in attr(env,start):
        yield chunk
    pass

class RamlMiddleware:
    def __init__(self, app, raml={}):
        self.app = app # A WSGI application callable.
        self.raml = raml
        pass
    def flatten(self, path_info):
        path_info = path_info.replace('{','_').replace('}','_')
        return path_info.replace('-','_').replace('/','_').replace('.','_')
    def __call__(self, env, start):
        print("100 OK LETS DO A CALL")
        flat_path_info = self.flatten(env['PATH_INFO'])
        print("200 OK LETS DO A CALL")
        attr = getattr(self.raml,'svr'+flat_path_info,None)
        print("300 OK LETS DO A CALL")
        if attr:
            print("310 OK LETS DO A CALL")
            return wrap(attr,env,start)
        print("400 OK LETS DO A CALL")
        return self.app(env,start)
        print("500 OK LETS DO A CALL")
    pass # end class RamlMiddleware
