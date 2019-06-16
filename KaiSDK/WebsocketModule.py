from KaiSDK.kai_sdk import KaiSDK
from KaiSDK.constants import Constants

import websockets
import asyncio
import logging

class WebSocketModule(KaiSDK):
    def __init__(self, moduleID, moduleSecret):
        self.initialize(moduleID, moduleSecret)

    async def dataListener(self):
        while True:
            try:
                self.handle(await self.webSocket.recv())
            except:
                logging.ERROR("Could not parse received data")
                continue

    def send(self, data):
        print("Sending data", data)
        print(type(data))
        asyncio.ensure_future(self.webSocket.send(data))

    async def setupConnections(self):
        self.webSocket = await websockets.connect(Constants.WebSockerURL, ping_interval=None)
        asyncio.ensure_future(self.dataListener())

    async def connect(self):
        if (not self.initalized):
            return None
        await self.setupConnections()
        self.sendAuth()

async def main():
    moduleID = ""
    moduleSecret = ""
    module = WebSocketModule(moduleID, moduleSecret)
    await module.connect()
    await asyncio.sleep(1000)

if __name__ == "__main__":
    print("Ran")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()