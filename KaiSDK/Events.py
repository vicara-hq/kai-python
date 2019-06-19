"""
Contains classes for different types of events that can be subscribed to from the Kai
"""

class GestureEvent:
    """
    Represents a Gesture performed on the kai (for eg: swipeLeft, sideSwipeRight, etc.)

    Attributes:

    gesture Enum representing the gesture (Refer to KaiSDK.DataTypes.Gesture)
    """
    def __init__(self, gesture):
        self.gesture = gesture


class LinearFlickEvent:
    def __init__(self, flick):
        self.flick = flick


class FingerPositionalEvent:
    """
    Informs about the state of each finger (open/closed)

    Attributes:

    Fingers (list): List of bools with state of each finger

    littleFinger (bool)

    ringFinger (bool)

    middleFinger (bool)

    indexFinger (bool)
    """
    def __init__(self, fingers):
        self.fingers = fingers
        self.littleFinger = fingers[0]
        self.ringFinger = fingers[1]
        self.middleFinger = fingers[2]
        self.indexFinger = fingers[3]


class AccelerometerEvent:
    """
    Accelerometer reading from Kai

    Attributes:

    accelerometer Vector3 (Refer to KaiSDK.DataTypes.Vector3)
    """
    def __init__(self, accelerometer):
        self.accelerometer = accelerometer


class GyroscopeEvent:
    """
    Gyroscope reading from Kai

    Attributes:

    gyroscope Vector3 (Refer to KaiSDK.DataTypes.Vector3)
    """
    def __init__(self, gyroscope):
        self.gyroscope = gyroscope


class MagnetometerEvent:
    """
    Magnetometer reading from Kai

    Attributes:

    accelerometer Vector3 (Refer to KaiSDK.DataTypes.Vector3)
    """
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
    """
    PYR reading from Kai

    Attributes:

    pitch (float)

    yaw (float)

    roll (float)
    """
    def __init__(self, pitch, yaw, roll):
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll


class QuaternionEvent:
    """
    Quaternion reading from Kai

    Attributes:

    quaternion Vector3 (Refer to KaiSDK.DataTypes.Quaternion)
    """
    def __init__(self, quaternion):
        self.quaternion = quaternion


class ErrorEvent:
    def __init__(self, code, error, message):
        self.code = code
        self.error = error
        self.message = message