import tornado
from handlers.prices import PriceHandler
from handlers.priceForm import PriceFormHandler
from handlers.favicon import Favicon

class MainHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("GET")
    def get(self):
        self.write("Hello, world")

    @staticmethod
    def getRoute():
        return (r"/", MainHandler)

