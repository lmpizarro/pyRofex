import asyncio
import tornado
from router import urls
from settings import settings

class Application:
    def __init__(self, urls, port):
        self.app = tornado.web.Application(urls, **settings)
        self.port = port

    async def run(self):
        self.app.listen(port=self.port)
        shutdown_event = asyncio.Event()
        await shutdown_event.wait()

if __name__ == "__main__":
    app = Application(urls=urls, port=8888)
    asyncio.run(app.run())



