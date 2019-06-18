from enum import IntFlag, Enum


class KaiCapabilities(IntFlag):
    GestureData = 1
    LinearFlickData = 2
    FingerShortcutData = 4
    FingerPositionalData = 8
    PYRData = 16
    QuaternionData = 32
    AccelerometerData = 64
    GyroscopeData = 128
    MagnetometerData = 256


class Gesture(Enum):
    swipeUp = 0
    swipeDown = 1
    swipeLeft = 2
    swipeRight = 3
    sideSwipeUp = 4
    sideSwipeDown = 5
    sideSwipeLeft = 6
    sideSwipeRight = 7
    pinch2Begin = 8
    pinch2End = 9
    grabBegin = 10
    grabEnd = 11
    pinch3Begin = 12
    pinch3End = 13
    dialBegin = 14
    dialEnd	= 15

class Hand(Enum):
    Left = 0
    Right = 1

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Quaternion:
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

