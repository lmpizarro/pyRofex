import tornado
from services.rava import preciosRava, Asset
from settings import Config
import json

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
        self.render(Config.getTemplatePath()+ "/precios.html", assets=None)

    async def post(self):
        tickers = self.get_argument("ticker")
        tickers = tickers.split(',')
        assets = [Asset(ticker, await preciosRava(ticker)) for ticker in tickers if len(ticker) > 0]
        self.render(Config.getTemplatePath()+ "/precios.html", assets=assets)

    def getRoute():
        return (r"/priceForm", PriceFormHandler)


class PriceHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("GET")
    async def get(self, tickers):
        tickers = [ticker for ticker in tickers.split(',') if len(ticker) >0]
        assets = [{ticker: await preciosRava(ticker)} for ticker in tickers]

        self.write(json.dumps(assets))

    @staticmethod
    def getRoute():
        return (r"/price/([0-9a-zA-z,]+)", PriceHandler)

