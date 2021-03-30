from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from app import webapp
from tornado.ioloop import IOLoop


s = HTTPServer(WSGIContainer(webapp))
s.listen(9900)  # 监听 9900 端口
IOLoop.current().start()
