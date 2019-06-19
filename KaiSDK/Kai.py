from KaiSDK.EventManager import EventManager


class Kai:
    def __init__(self, id = 0, capabilities = 0, hand = 0):
        self.id = 0
        self.capabilities = 0
        self.hand = 0
        self.eventManager = EventManager()

    def register_event_listener(self, event, listener):
        """

        :param event: Event Class that listener is subscribing to
        (Refer to KaiSDK.Events for event classes)
        :param listener: A callback function to be called when the event is
        received from the kai
        :return:
        """
        self.eventManager.add_listener(event, listener)

    def notify_event(self, event):
        self.eventManager.update(event)

    def set_capabilities(self, capabilities):
        self.capabilities = self.capabilities | capabilities

    def unset_capabilities(self, capabilities):
        self.capabilities = self.capabilities & ~capabilities
