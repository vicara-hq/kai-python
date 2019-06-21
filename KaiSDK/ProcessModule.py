"""
Used to create a Process Module
"""

from KaiSDK.kai_sdk import KaiSDK
from KaiSDK.constants import Constants

import websocket
import threading
import traceback


class ProcessModule(KaiSDK):
    """
    Creates a Kai Process Module

    Attributes:

    DefaultKai (Kai): Represents the Default Kai connected

    DefaultLeftKai (Kai): Represents the default kai for the left hand

    DefaultRightKai (Kai): Represents the default kai for the right hand

    AnyKai (Kai): Represents All Kais connected. Useful for registering an event listener
    for data from all connected Kais
    """

    def __init__(self):
        KaiSDK.__init__(self)

    def receive_data(self):
        data = ""
        while True:
            inp = input()
            if inp:
                data += inp
            else:
                break
        return data

    def send(self, data):
        print(data)

    def create_connection(self):
        pass

    def close_connection(self):
        pass


