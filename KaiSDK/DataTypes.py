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
    SwipeUp = 0
    SwipeDown = 1
    SwipeLeft = 2
    SwipeRight = 3
    SideSwipeUp = 4
    SideSwipeDown = 5
    SideSwipeLeft = 6
    SideSwipeRight = 7
    Pinch2Begin = 8
    Pinch2End = 9
    GrabBegin = 10
    GrabEnd = 11
    Pinch3Begin = 12
    Pinch3End = 13
    DialBegin = 14
    DialEnd	= 15

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

