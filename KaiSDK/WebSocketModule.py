"""
Used to create a Kai Web Socket Module
"""

from KaiSDK.kai_sdk import KaiSDK
from KaiSDK.constants import Constants

import websocket
import threading
import traceback

class WebSocketModule(KaiSDK):
    """
    Creates a Kai Websocket module

    Attributes:

    DefaultKai (Kai): Represents the Default Kai connected

    DefaultLeftKai (Kai): Represents the default kai for the left hand

    DefaultRightKai (Kai): Represents the default kai for the right hand

    AnyKai (Kai): Represents All Kais connected. Useful for registering an event listener
    for data from all connected Kais
    """
    def __init__(self):
        self.running = False
        self.webSocket = None
        KaiSDK.__init__(self)

    def receive_data(self):
        return self.webSocket.recv()

    def send(self, data):
        self.webSocket.send(data)

    def close(self):
        """
        Closes the socket connection to the Kai SDK
        :return: None
        """
        if (self.running):
            self.running = False

            # Trigger a recv() for the listener so it closes (seems kind of hacky)
            self.getSDKVersion()
            self.webSocket.close()

    def create_connection(self):
        self.webSocket = websocket.create_connection(Constants.WebSockerURL)

    def close_connection(self):
        self.webSocket.close()


