from KaiSDK.kai_sdk import KaiSDK
from KaiSDK.constants import Constants

import websocket
import threading
import traceback

class WebSocketModule(KaiSDK):
    def dataListener(self):
        while self.running:
            try:
                self.handle(self.webSocket.recv())
            except:
                print(traceback.format_exc())
                self.close()

    def send(self, data):
        self.webSocket.send(data)

    def close(self):
        if (self.running):
            self.running = False

            # Trigger a recv() for the listener so it closes (seems kind of hacky)
            self.getSDKVersion()
            self.webSocket.close()

    def connect(self, moduleID, moduleSecret):
        self.initialize(moduleID, moduleSecret)
        self.webSocket = websocket.create_connection(Constants.WebSockerURL)
        self.sendAuth()
        self.handle(self.webSocket.recv())
        self.running = True
        self.socketListener = threading.Thread(target = self.dataListener)
        self.socketListener.start()
