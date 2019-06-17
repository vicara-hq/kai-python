from KaiSDK.kai_sdk import KaiSDK
from KaiSDK.constants import Constants

import websockets
import asyncio
import logging

class WebSocketModule(KaiSDK):
    async def dataListener(self):
        while True:
            try:
                self.handle(await self.webSocket.recv())
            except:
                logging.ERROR("Could not parse received data")
                continue

    def send(self, data):
        asyncio.ensure_future(self.webSocket.send(data))

    async def setupConnections(self):
        self.webSocket = await websockets.connect(Constants.WebSockerURL, ping_interval=None)

    async def connect(self, moduleID, moduleSecret):
        self.initialize(moduleID, moduleSecret)
        await self.setupConnections()
        self.sendAuth()

        # Handle auth response
        self.handle(await self.webSocket.recv())

        if (self.authenticated):
            asyncio.ensure_future(self.dataListener())
        else:
            return False


async def main():
    import os
    from KaiSDK.DataTypes import KaiCapabilities
    moduleID = os.environ.get("MODULE_ID")
    moduleSecret = os.environ.get("MODULE_SECRET")
    module = WebSocketModule()
    await module.connect(moduleID, moduleSecret)
    module.setCapabilities(module.DefaultKai, KaiCapabilities.GestureData)
    await asyncio.sleep(1000)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()