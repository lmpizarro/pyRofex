import tornado
from services.rava import preciosRava, Asset
from settings import Config

class PriceFormHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("GET", "POST")
    def get(self):
        self.render(Config.getTemplatePath('ravaPrices')+ "/precios.html", assets=None)

    async def post(self):
        tickers = self.get_argument("ticker")
        tickers = tickers.split(',')
        assets = [Asset(ticker, await preciosRava(ticker)) for ticker in tickers if len(ticker) > 0]
        self.render(Config.getTemplatePath('ravaPrices')+ "/precios.html", assets=assets)

    def getRoute():
        return (r"/priceForm", PriceFormHandler)


