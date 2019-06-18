import os
import time

from KaiSDK.WebsocketModule import WebSocketModule
from KaiSDK.DataTypes import KaiCapabilities
import KaiSDK.Events as Events

def gestureEvent(ev):
    print(ev.gesture)


moduleID = os.environ.get("MODULE_ID")
moduleSecret = os.environ.get("MODULE_SECRET")
module = WebSocketModule()
module.connect(moduleID, moduleSecret)
module.setCapabilities(module.DefaultKai, KaiCapabilities.GestureData)
module.DefaultKai.register_event_listener(Events.GestureEvent, gestureEvent)
time.sleep(10)
module.close()