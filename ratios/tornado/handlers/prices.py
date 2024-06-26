import tornado
from services.rava import priceRavaList
import json

class PriceHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("GET")
    async def get(self, tickers):
        tickers = [ticker for ticker in tickers.split(',') if len(ticker) >0]
        assets = {'assets': await priceRavaList(tickers)}

        self.write(json.dumps(assets))

    @staticmethod
    def getRoute():
        return (r"/price/([0-9a-zA-z,]+)", PriceHandler)

