#!/usr/bin/python
from __future__ import print_function

def wrap(attr,env,start):
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
        flat_path_info = self.flatten(env['PATH_INFO'])
        attr = getattr(self.raml,'rpc'+flat_path_info,None)
        if attr:
            return wrap(attr,env,start)
        return self.app(env,start)
    pass # end class RamlMiddleware
