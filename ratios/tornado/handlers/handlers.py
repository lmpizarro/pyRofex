import tornado
from services.rava import preciosRava, Asset
from settings import Config
import numpy as np

class MainHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("GET")
    def get(self):
        self.write("Hello, world")

    @staticmethod
    def getRoute():
        return (r"/", MainHandler)

class PriceFormHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("GET", "POST")
    def get(self):
        self.render(Config.getTemplatePath()+ "/precios.html", asset=None)

    def post(self):
        ticker = self.get_argument("ticker")
        precio = preciosRava(ticker)
        self.render(Config.getTemplatePath()+ "/precios.html", asset=Asset(ticker, precio))

    def getRoute():
        return (r"/priceForm", PriceFormHandler)


class PriceHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("GET")
    def get(self, ticker):
        precio = preciosRava(ticker)
        self.write(f"ticker {ticker} precio {precio}")

    @staticmethod
    def getRoute():
        return (r"/price/([0-9a-zA-z]+)", PriceHandler)

