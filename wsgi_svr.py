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
    def __call__(self, environ, start_response):
        flat_path_info = self.flatten(environ['PATH_INFO'])
        attr = getattr(self.raml,'rpc'+flat_path_info,None)
        if attr:
            return wrap(attr,environ,start_response)
        return self.app(environ,start_response)
    #for chunk in self.application(environ, start_response):
    #  yield chunk.lower()
    pass # end class RamlMiddleware

def application(env, start_response):
    if env['PATH_INFO'] == '/':
        start_response('200 OK', [('Content-Type', 'text/html')])
        return ["<b>hello world</b>"]
    else:
        start_response('404 Not Found', [('Content-Type', 'text/html')])
        return ['<h1>Not Found</h1>']

class XX:
    def rpc_qaz(_,e,s):
        print("QAZ", repr((e,s)))
        s('200 OK', [('Content-Type', 'text/html')])
        return ["<b>hello worldxxxx</b>"]
        return
    #return ["<b>hello world</b>"]
    pass

if __name__ == '__main__':
    from gevent.pywsgi import WSGIServer
    app = RamlMiddleware(application,XX())
    try:
        print('Serving on https://:8443')
        WSGIServer(('', 8443), app, keyfile='server.key', certfile='server.crt').start()
    except:
        print("ERR")
        pass
    print('Serving on  http://:8080')
    WSGIServer(('', 8080), app).serve_forever()
    
