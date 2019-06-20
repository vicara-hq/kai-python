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
        self.initialized = False
        self.authenticated = False

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
        """
        Closes the socket connection to the Kai SDK
        :return: None
        """
        if (self.running):
            self.running = False

            # Trigger a recv() for the listener so it closes (seems kind of hacky)
            self.getSDKVersion()
            self.webSocket.close()

    def connect(self, moduleID, moduleSecret):
        """
        Connects to the SDK and authenticates using the given moduleID and moduleSecret
        :param moduleID: module ID of your Kai module
        :type moduleID: str
        :param moduleSecret:  module secret of your kai module
        :type moduleSecret str
        :return: True if successfully connected and authenticated, otherwise False
        :rtype: bool
        """
        self.initialize(moduleID, moduleSecret)
        self.webSocket = websocket.create_connection(Constants.WebSockerURL)
        self.sendAuth()
        self.handle(self.webSocket.recv())
        if (self.authenticated):
            self.running = True
            self.socketListener = threading.Thread(target = self.dataListener)
            self.socketListener.start()
            return True
        return False
