from KaiSDK.constants import Constants
from KaiSDK.DataTypes import Hand, KaiCapabilities, Gesture, Quaternion, Vector3
import KaiSDK.Events as Events

from KaiSDK.Kai import Kai
import json
import traceback
import threading
nomenclature = ['alpha', 'beta', 'gamma','delta','epsilon','zeta', 'eta','theta']


class KaiSDK:
    ConnectedKais = [Kai(name=x) for x in nomenclature]
    ForegroundProcess = ""

    myKai = ConnectedKais[0]
    DefaultKai = myKai
    DefaultLeftKai = myKai
    DefaultRightKai = myKai
    AnyKai = myKai

    def __init__(self):
        self.initialized = False
        self.authenticated = False
        self.running = False

    def initialize(self, moduleID, moduleSecret):
        self.moduleID = moduleID
        self.moduleSecret = moduleSecret
        self.initalized = True

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
        self.create_connection() #redundant
        self.sendAuth()
        self.handle(self.receive_data())
        if self.authenticated:
            print("KaiSDK successfully connected")
            self.running = True
            self.dataListener = threading.Thread(target=self.listener_thread)
            self.dataListener.start()
            print("started event listening")
            return True
        return False

    def create_connection(self):
        return NotImplementedError

    def close_connection(self):
        return NotImplementedError

    def close(self):
        if self.running:
            self.running = False

            # Trigger a receive_data() for the dataListener so it closes (seems kind of hacky)
            self.getSDKVersion()
            self.close_connection()

    @staticmethod
    def getKaiByID(kaiID):
        if (kaiID >= 8):
            return None
        return KaiSDK.ConnectedKais[kaiID]

    def send(self, json):
        return NotImplementedError

    def receive_data(self):
        return NotImplementedError

    def listener_thread(self):
        while self.running:
            try:
                self.handle(self.receive_data())
            except:
                print(traceback.format_exc())
                self.close()

    def sendAuth(self):
        print("Authentication in progress")
        obj = dict()
        obj[Constants.Type] = Constants.Authentication
        print(Constants.Authentication)
        obj[Constants.ModuleId] = self.moduleID
        print(self.moduleID)
        print("Authentication successful")
        obj[Constants.ModuleSecret] = self.moduleSecret

        self.send(json.dumps(obj))

    def getConnectedKais(self):
        obj = dict()
        obj[Constants.Type] = Constants.ListConnectedKais
        self.send(json.dumps(obj))
        return Constants.ListConnectedKais

    def getSDKVersion(self):
        obj = dict()
        obj[Constants.Type] = Constants.GetSDKVersion
        self.send(json.dumps(obj))
        return Constants.GetSDKVersion

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
        kai.unset_capabilities(capabilities)

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

        try:
            obj = json.loads(data)
        except json.decoder.JSONDecodeError:
            return

        if not obj.get(Constants.Success):
            self.decodeSdkError(obj)

        resType = obj.get(Constants.Type)

        if (not resType):
            return False

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
        foregroundProcess = obj.get(Constants.ForegroundProcess)

        kaiID = obj.get(Constants.KaiID)
        kai = KaiSDK.ConnectedKais[kaiID]
        defaultKai = obj.get(Constants.DefaultKai) or obj.get(Constants.Default)
        defaultLeftKai = obj.get(Constants.DefaultLeftKai) or obj.get(Constants.DefaultLeft)
        defaultRightKai = obj.get(Constants.DefaultRightKai) or obj.get(Constants.DefaultRight)

        dataList = obj.get(Constants.Data)

        for data in dataList:
            dataType = data[Constants.Type]

            if dataType == Constants.GestureData:
                event = KaiSDK.parseGestureData(data)
            elif dataType == Constants.FingerShortcutData:
                event = KaiSDK.parseFingerShortcutData(data)
            elif dataType == Constants.PYRData:
                event = KaiSDK.parsePYRData(data)
            elif dataType == Constants.QuaternionData:
                event = KaiSDK.parseQuaternionData(data)
            elif dataType == Constants.LinearFlickData:
                event = KaiSDK.parseLinearFlickData(data)
            elif dataType == Constants.FingerPositionalData:
                event = KaiSDK.parseFingerPositionalData(data)
            elif dataType == Constants.AccelerometerData:
                event = KaiSDK.parseAccelerometerData(data)
            elif dataType == Constants.GyroscopeData:
                event = KaiSDK.parseGyroscopeData(data)
            elif dataType == Constants.MagnetometerData:
                event = KaiSDK.parseMagnetometerData(data)
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
        gestureType = obj.get(Constants.Gesture)

        try:
            gesture = Gesture[gestureType]
            return Events.GestureEvent(gesture)
        except KeyError:
            return

    @staticmethod
    def parseFingerShortcutData(obj):
        fingers = obj.get(Constants.Fingers)
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
    def parseAccelerometerData(obj):
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
        vectorObj = obj[Constants.Magnetometer]
        x = vectorObj[Constants.X]
        y = vectorObj[Constants.Y]
        z = vectorObj[Constants.Z]
        return Events.MagnetometerEvent(Vector3(x, y, z))

    @staticmethod
    def decodeSdkError(error):
        return NotImplementedError

    def decodeAuthentication(self, auth):
        if auth.get(Constants.Success):
            self.authenticated = True
            self.getConnectedKais()
            return True
        else:
            return False

    def decodeConnectedKais(self, obj):
        for token in obj[Constants.Kais]:
            self.decodeKaiConnected(token)

    def decodeKaiConnected(self, obj):
        kaiID = obj.get(Constants.KaiID)
        hand = obj.get(Constants.Hand)

        defaultKai = obj.get(Constants.DefaultKai) or obj.get(Constants.Default)
        defaultLeftKai = obj.get(Constants.DefaultLeftKai) or obj.get(Constants.DefaultLeft)
        defaultRightKai = obj.get(Constants.DefaultRightKai) or obj.get(Constants.DefaultRight)

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
