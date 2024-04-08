import tornado
from handlers.prices import PriceHandler
from handlers.priceForm import PriceFormHandler

class MainHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("GET")
    def get(self):
        self.write("Hello, world")

    @staticmethod
    def getRoute():
        return (r"/", MainHandler)

