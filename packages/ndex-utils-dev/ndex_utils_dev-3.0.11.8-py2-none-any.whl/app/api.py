#!/usr/local/bin/python
import sys
import argparse
import bottle
import app
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from bottle import Bottle, redirect, static_file, request

bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024

api = Bottle()

log = app.get_logger('api')

@api.get('/')
def index():
    redirect('/ui/index.html')

@api.get('/ui/<filepath:path>')
def static(filepath):
    return static_file(filepath, root=app.static_path)

@api.get('/api/message/:message')
def api_message(message):
    return {
        'message': message
    }

# run the web server
def main():
    status = 0
    parser = argparse.ArgumentParser()
    parser.add_argument('port', nargs='?', type=int, help='HTTP port', default=80)
    args = parser.parse_args()

    print 'starting web server on port %s' % args.port
    print 'press control-c to quit'
    try:
        server = WSGIServer(('0.0.0.0', args.port), api, handler_class=WebSocketHandler)
        log.info('entering main loop')
        server.serve_forever()
    except KeyboardInterrupt:
        log.info('exiting main loop')
    except Exception as e:
        str = 'could not start web server: %s' % e
        log.error(str)
        print str
        status = 1

    log.info('exiting with status %d', status)
    return status

if __name__ == '__main__':
    sys.exit(main())