import tornado

from handlers.handlers import (
    MainHandler,
    PriceFormHandler,
    PriceHandler
)
from handlers.favicon import Favicon

from settings import settings

urls =[
        MainHandler.getRoute(),
        PriceFormHandler.getRoute(),
        PriceHandler.getRoute(),
        Favicon.getRoute(),
    ]