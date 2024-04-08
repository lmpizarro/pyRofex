import tornado
from handlers.prices import PriceHandler
from handlers.priceForm import PriceFormHandler
from handlers.favicon import Favicon

class MainHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("GET", "POST")
    def get(self):
        self.render("base.html", message="H e L l O")

    def post(self):
        self.write("hola")
        
    @staticmethod
    def getRoute():
        return (r"/", MainHandler)

