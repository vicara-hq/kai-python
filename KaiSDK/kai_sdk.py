from KaiSDK.constants import Constants
from KaiSDK.DataTypes import Hand, KaiCapabilities, Gesture, Quaternion, Vector3
import KaiSDK.Events as Events

from KaiSDK.Kai import Kai
import json
import logging

logging.basicConfig(level=logging.INFO)

class KaiSDK:
    ConnectedKais = [Kai() for i in range(8)]
    ForegroundProcess = ""

    DefaultKai = Kai()
    DefaultLeftKai = Kai()
    DefaultRightKai = Kai()
    AnyKai = Kai()

    def initialize(self, moduleID, moduleSecret):
        self.moduleID = moduleID
        self.moduleSecret = moduleSecret
        self.initalized = True

    @staticmethod
    def getKaiByID(kaiID):
        if (kaiID >= 8):
            return None
        return KaiSDK.connectedKais[kaiID]

    def sendAuth(self):
        obj = dict()
        obj[Constants.Type] = Constants.Authentication
        obj[Constants.ModuleId] = self.moduleID
        obj[Constants.ModuleSecret] = self.moduleSecret

        self.send(json.dumps(obj))

    def getConnectedKais(self):
        obj = dict()
        obj[Constants.Type] = Constants.ListConnectedKais
        self.send(json.dumps(obj))

    def setCapabilities(self, kai, capabilities):
        kai.set_capabilities(capabilities)

        if (not self.authenticated):
            return

        obj = dict()
        obj[Constants.Type] = Constants.SetCapabilities

        if (kai is KaiSDK.DefaultKai):
            obj[Constants.KaiID] = Constants.Default
        elif (kai is KaiSDK.DefaultLeftKai):
            obj[Constants.KaiID] = Constants.DefaultLeft
        elif (kai is KaiSDK.DefaultRightKai):
            obj[Constants.KaiID] = Constants.DefaultRight
        else:
            obj[Constants.KaiID] = kai.id

        obj[Constants.GestureData] = KaiCapabilities.GestureData in capabilities
        obj[Constants.LinearFlickData] = KaiCapabilities.LinearFlickData in capabilities
        obj[Constants.FingerShortcutData] = KaiCapabilities.FingerShortcutData in capabilities
        obj[Constants.PYRData] = KaiCapabilities.PYRData in capabilities
        obj[Constants.QuaternionData] = KaiCapabilities.QuaternionData in capabilities
        obj[Constants.AccelerometerData] = KaiCapabilities.AccelerometerData in capabilities
        obj[Constants.GyroscopeData] = KaiCapabilities.GyroscopeData in capabilities
        obj[Constants.MagnetometerData] = KaiCapabilities.MagnetometerData in capabilities

        self.send(json.dumps(obj))

    def unsetCapabilities(self, kai, capabilities):
        kai.capabilities |= capabilities

        if (not self.authenticated):
            return

        obj = dict()
        obj[Constants.Type] = Constants.SetCapabilities

        if (kai is KaiSDK.DefaultKai):
            obj[Constants.KaiID] = Constants.Default
        elif (kai is KaiSDK.DefaultLeftKai):
            obj[Constants.KaiID] = Constants.DefaultLeft
        elif (kai is KaiSDK.DefaultRightKai):
            obj[Constants.KaiID] = Constants.DefaultRight
        else:
            obj[Constants.KaiID] = kai.id

        obj[Constants.GestureData] = KaiCapabilities.GestureData not in capabilities
        obj[Constants.LinearFlickData] = KaiCapabilities.LinearFlickData not in capabilities
        obj[Constants.FingerShortcutData] = KaiCapabilities.FingerShortcutData not in capabilities
        obj[Constants.PYRData] = KaiCapabilities.PYRData not in capabilities
        obj[Constants.QuaternionData] = KaiCapabilities.QuaternionData not in capabilities
        obj[Constants.AccelerometerData] = KaiCapabilities.AccelerometerData not in capabilities
        obj[Constants.GyroscopeData] = KaiCapabilities.GyroscopeData not in capabilities
        obj[Constants.MagnetometerData] = KaiCapabilities.MagnetometerData not in capabilities

        self.send(json.dumps(obj))

    def handle(self, data):
        if (not self.initalized):
            return False

        obj = json.loads(data)
        logging.info(obj)
        if not obj.get(Constants.Success):
            self.decodeSdkError(obj)

        resType = obj[Constants.Type]

        if resType == Constants.Authentication:
            self.decodeAuthentication(obj)
        elif resType == Constants.IncomingData:
            KaiSDK.decodeIncomingData(obj)
        elif resType == Constants.ListConnectedKais:
            self.decodeConnectedKais(obj)
        elif resType == Constants.KaiConnected:
            self.decodeKaiConnected(obj)
        else:
            # TODO Handle Unkown data type
            return False

    @staticmethod
    def decodeIncomingData(obj):
        foregroundProcess = obj[Constants.ForegroundProcess]

        kaiID = obj[Constants.KaiID]
        kai = KaiSDK.ConnectedKais[Constants.KaiID]
        defaultKai = obj[Constants.DefaultKai]
        defaultLeftKai = obj[Constants.DefaultLeftKai]
        defaultRightKai = obj[Constants.DefaultRightKai]

        dataList = obj[Constants.Data]

        for data in dataList:
            dataType = data[Constants.Type]


        if dataType == Constants.GestureData:
            event = KaiSDK.parseGestureData(obj)
        elif dataType == Constants.FingerShortcutData:
            event = KaiSDK.parseFingerShortcutData(obj)
        elif dataType == Constants.PYRData:
            event = KaiSDK.parsePYRData(obj)
        elif dataType == Constants.QuaternionData:
            event = KaiSDK.parseQuaternionData(obj)
        elif dataType == Constants.LinearFlickData:
            event = KaiSDK.parseLinearFlickData(obj)
        elif dataType == Constants.FingerPositionalData:
            event = KaiSDK.parseFingerPositionalData(obj)
        elif dataType == Constants.AccelerometerData:
            event = KaiSDK.parseAccelerometerData(obj)
        elif dataType == Constants.GyroscopeData:
            event = KaiSDK.parseGyroscopeData(obj)
        elif dataType == Constants.MagnetometerData:
            event = KaiSDK.parseMagnetometerData(obj)
        else:
            return

        kai.notify_event(event)

        if (defaultKai):
            KaiSDK.DefaultKai.notify_event(event)
        if (defaultRightKai):
            KaiSDK.DefaultRightKai.notify_event(event)
        if (defaultLeftKai):
            KaiSDK.DefaultLeftKai.notify_event(event)
        KaiSDK.AnyKai.notify_event(event)

    @staticmethod
    def parseGestureData(obj):
        gestureType = obj[Constants.Gesture]

        try:
            gesture = Gesture[gestureType]
            return Events.GestureEvent(gesture)
        except KeyError:
            return

    @staticmethod
    def parseFingerShortcutData(obj):
        fingers = obj[Constants.Fingers]
        return Events.FingerShortcutEvent(fingers)

    @staticmethod
    def parsePYRData(obj):
        pitch = obj[Constants.Pitch]
        yaw = obj[Constants.Yaw]
        roll = obj[Constants.Roll]
        return Events.PYREvent(pitch, yaw, roll)

    @staticmethod
    def parseQuaternionData(obj):
        quaternionObj = obj[Constants.Quaternion]
        w = quaternionObj[Constants.W]
        x = quaternionObj[Constants.X]
        y = quaternionObj[Constants.Y]
        z = quaternionObj[Constants.Z]
        return Events.QuaternionEvent(Quaternion(w, x, y, z))

    @staticmethod
    def parseLinearFlickData(obj):
        flick = obj[Constants.Flick]
        return Events.LinearFlickEvent(flick)

    @staticmethod
    def parseFingerPositionalData(obj):
        fingers = obj[Constants.Fingers]
        return Events.FingerPositionalEvent(fingers)

    @staticmethod
    def parseAcceleromterData(obj):
        vectorObj = obj[Constants.Accelerometer]
        x = vectorObj[Constants.X]
        y = vectorObj[Constants.Y]
        z = vectorObj[Constants.Z]
        return Events.AccelerometerEvent(Vector3(x, y, z))

    @staticmethod
    def parseGyroscopeData(obj):
        vectorObj = obj[Constants.Gyroscope]
        x = vectorObj[Constants.X]
        y = vectorObj[Constants.Y]
        z = vectorObj[Constants.Z]
        return Events.GyroscopeEvent(Vector3(x, y, z))

    @staticmethod
    def parseMagnetometerData(obj):
        vectorObj = obj[Constants.Gyroscope]
        x = vectorObj[Constants.X]
        y = vectorObj[Constants.Y]
        z = vectorObj[Constants.Z]
        return Events.MagnetometerEvent(Vector3(x, y, z))

    @staticmethod
    def decodeSdkError(error):
        return NotImplementedError

    def decodeAuthentication(self, auth):
        if auth.get(Constants.Success):
            logging.info("Authentication successful")
            self.authenticated = True
            self.getConnectedKais()
            return True
        else:
            logging.error("Authentication Failed")
            return False

    def decodeConnectedKais(self, obj):
        for token in obj[Constants.Kais]:
            self.decodeKaiConnected(token)

    def decodeKaiConnected(self, obj):
        kaiID = obj.get(Constants.KaiID)
        hand = obj.get(Constants.Hand)

        defaultKai = Constants.DefaultKai
        defaultLeftKai = Constants.DefaultLeftKai
        defaultRightKai = Constants.DefaultRightKai

        kaiSerialNumber = Constants.KaiSerialNumber

        try:
            handEnum = Hand[hand]
        except KeyError:
            handEnum = Hand.Left

        if (defaultKai):
            KaiSDK.DefaultKai.id = kaiID
            KaiSDK.DefaultKai.hand = handEnum

        if (defaultLeftKai):
            KaiSDK.DefaultLeftKai.id = kaiID
            KaiSDK.DefaultLeftKai.hand = handEnum

        if (defaultRightKai):
            KaiSDK.DefaultRightKai.id = kaiID
            KaiSDK.DefaultRightKai.hand = handEnum

        KaiSDK.ConnectedKais[kaiID] = Kai(id=kaiID, hand=handEnum)

        if (defaultKai or defaultRightKai or defaultLeftKai):
            self.ResetDefaultCapabilities()

    def ResetDefaultCapabilities(self):
        if (KaiSDK.DefaultKai.capabilities != 0):
            self.setCapabilities(KaiSDK.DefaultKai, KaiSDK.DefaultKai.capabilities)

        if (KaiSDK.DefaultLeftKai.capabilities != 0):
            self.setCapabilities(KaiSDK.DefaultKai, KaiSDK.DefaultLeftKai.capabilities)

        if (KaiSDK.DefaultRightKai.capabilities != 0):
            self.setCapabilities(KaiSDK.DefaultKai, KaiSDK.DefaultRightKai.capabilities)
