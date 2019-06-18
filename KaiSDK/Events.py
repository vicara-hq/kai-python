class GestureEvent:
    def __init__(self, gesture):
        self.gesture = gesture


class LinearFlickEvent:
    def __init__(self, flick):
        self.flick = flick


class FingerPositionalEvent:
    def __init__(self, fingers):
        self.fingers = fingers
        self.littleFinger = fingers[0]
        self.ringFinger = fingers[1]
        self.middleFinger = fingers[2]
        self.indexFinger = fingers[3]


class AccelerometerEvent:
    def __init__(self, accelerometer):
        self.accelerometer = accelerometer


class GyroscopeEvent:
    def __init__(self, gyroscope):
        self.gyroscope = gyroscope


class MagnetometerEvent:
    def __init__(self, magnetometer):
        self.magnetometer = magnetometer


class UnknownGestureEvent:
    def __init__(self, gesture):
        self.gesture = gesture


class FingerShortcutEvent:
    def __init__(self, fingers):
        self.fingers = fingers
        self.littleFinger = fingers[0]
        self.ringFinger = fingers[1]
        self.middleFinger = fingers[2]
        self.indexFinger = fingers[3]


class PYREvent:
    def __init__(self, pitch, yaw, roll):
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll


class QuaternionEvent:
    def __init__(self, quaternion):
        self.quaternion = quaternion


class ErrorEvent:
    def __init__(self, code, error, message):
        self.code = code
        self.error = error
        self.message = message