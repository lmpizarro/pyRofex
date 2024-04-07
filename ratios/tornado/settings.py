import os

APP_NAME = "tornado"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE_PATH = os.path.join(BASE_DIR, APP_NAME, "templates")

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": TEMPLATE_PATH,
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "login_url": "/login",
    "xsrf_cookies": True,
}


class Config:
    @staticmethod
    def getTemplatePath():
        return TEMPLATE_PATH


print('[settings] TEMPLATE_PATH ', Config.getTemplatePath())