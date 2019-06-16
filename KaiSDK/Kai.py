from KaiSDK.EventManager import EventManager


class Kai:
    def __init__(self, id = 0, capabilities = 0, hand = 0):
        self.id = 0
        self.capabilities = 0
        self.hand = 0
        self.eventManager = EventManager()

    def register_event_listener(self, event, listener):
        self.eventManager.add_listener(event, listener)

    def set_capabilities(self, capabilities):
        self.capabilities = self.capabilities | capabilities
        return NotImplementedError

    def unset_capabilities(self, capabilities):
        self.capabilities = self.capabilities & ~capabilities
        return NotImplementedError
