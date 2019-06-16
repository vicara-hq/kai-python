from KaiSDK.constants import Constants
from KaiSDK.DataTypes import Hand

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
    AnyKai = None

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
        self.send(json.dump(obj))

    def handle(self, data):
        if (not self.initalized):
            return False

        obj = json.loads(data)

        if not obj.get(Constants.Success):
            self.decodeSdkError(obj)

        resType = obj[Constants.Type]

        if resType == Constants.Authentication:
            self.decodeAuthentication(obj)
        elif resType == Constants.IncomingData:
            self.decodeIncomingData(obj)
        elif resType == Constants.ListConnectedKais:
            self.decodeConnectedKais(obj)
        elif resType == Constants.KaiConnected:
            self.decodeKaiConnected(obj)
        else:
            # TODO Handle Unkown data type
            return False

    def decodeSdkError(self, error):
        return NotImplementedError

    def decodeAuthentication(self, auth):
        if auth.get(Constants.Success):
            logging.info("Authentication successful")
            return True
        else:
            logging.error("Authentication Failed")
            return False

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
            KaiSDK.ResetDefaultCapabilities()

    @staticmethod
    def ResetDefaultCapabilities():
        if (KaiSDK.DefaultKai.capabilities != 0):
            KaiSDK.DefaultKai.set_capabilities(KaiSDK.DefaultKai, KaiSDK.DefaultKai.capabilities)

        if (KaiSDK.DefaultLeftKai.capabilities != 0):
            KaiSDK.DefaultLeftKai.set_capabilities(KaiSDK.DefaultKai, KaiSDK.DefaultLeftKai.capabilities)

        if (KaiSDK.DefaultRightKai.capabilities != 0):
            KaiSDK.DefaultRightKai.set_capabilities(KaiSDK.DefaultKai, KaiSDK.DefaultRightKai.capabilities)
