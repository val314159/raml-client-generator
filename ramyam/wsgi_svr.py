#!/usr/bin/python
from __future__ import print_function
from gevent import monkey;monkey.patch_all()
import os, traceback as tb
from gevent.pywsgi import WSGIServer

from .wsgi_mid import wrap, RamlMiddleware

Offset = int(os.environ.get('PORT_OFFSET','8000'))

def spew():
    print("*"*40)
    tb.print_exc()
    print("*"*40)
    raise

def serve_https(app,port,dd):
    print('Serving on https://:'+str(port))
    try:    return WSGIServer(('', port), app,
                              keyfile =dd+'server.key',
                              certfile=dd+'server.crt')
    except: raise spew()

def serve_http(app,port):
    print('Serving on  http://:'+str(port))
    try:    return WSGIServer(('', port), app).serve_forever()
    except: raise spew()

def serve_both(app,dd):
    serve_https(app,Offset+443,dd).start()
    return serve_http(app,Offset+80)

def main(raml_obj=None):
    def test_application(env, start_response):
        if env['PATH_INFO'] == '/':
            start_response('200 OK', [('Content-Type', 'text/html')])
            return ["<b>hello world</b>"]
        else:
            start_response('404 Not Found', [('Content-Type', 'text/html')])
            return ['<h1>Not Found</h1>']
        pass
    class TestRamlObject:
        def rpc_qaz(_,env,start):
            print("QAZ", repr((env,start)))
            start('200 OK', [('Content-Type', 'text/html')])
            return ["<b>hello worldxxxx</b>"]
        pass
    raml_obj = raml_obj or TestRamlObject
    serve_both( RamlMiddleware(test_application,raml_obj()),
                os.environ.get('DD','data/') ).serve_forever()

if __name__ == '__main__':main()
