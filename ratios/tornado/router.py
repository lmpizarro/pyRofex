from handlers.handlers import (
    MainHandler,
    PriceFormHandler,
    PriceHandler,
    Favicon
)

urls =[
        MainHandler.getRoute(),
        PriceFormHandler.getRoute(),
        PriceHandler.getRoute(),
        Favicon.getRoute(),
    ]