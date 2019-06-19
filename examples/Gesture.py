"""
Example program for receiving gesture events and accelerometer readings from Kai
"""

import os
import time

from KaiSDK.WebSocketModule import WebSocketModule
from KaiSDK.DataTypes import KaiCapabilities
import KaiSDK.Events as Events

# Event listener functions
def gestureEvent(ev):
    print(ev.gesture)

def accelerometerEv(ev):
    print(ev.accelerometer.x)

moduleID = os.environ.get("MODULE_ID")
moduleSecret = os.environ.get("MODULE_SECRET")

# Create a WS module and connect to the SDK
module = WebSocketModule()
module.connect(moduleID, moduleSecret)

# Set the default Kai to record gestures and accelerometer readings
module.setCapabilities(module.DefaultKai, KaiCapabilities.GestureData | KaiCapabilities.AccelerometerData)

# Register event listeners
module.DefaultKai.register_event_listener(Events.GestureEvent, gestureEvent)
module.DefaultLeftKai.register_event_listener(Events.AccelerometerEvent, accelerometerEv)

time.sleep(30) # Delay for testing purposes

# Save Kai battery by unsetting capabilities which are not required anymore
module.unsetCapabilities(module.DefaultKai, KaiCapabilities.AccelerometerData)

time.sleep(30)

module.close()