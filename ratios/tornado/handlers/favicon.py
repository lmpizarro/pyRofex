import tornado
from settings import settings

class Favicon(tornado.web.RequestHandler):
    @staticmethod
    def getRoute():
        return (r"/(favicon.ico)", tornado.web.StaticFileHandler,
                dict(path=settings['static_path']))