from ds.vortex import customLogger

logger = customLogger.getCustomLogger()


class VortexSignal(object):
    def __init__(self):
        self.events = set()

    def __len__(self):
        return len(self.events)

    def removeEvent(self, event):
        try:
            self.events.remove(event)
            logger.debug("Removed event:: %s" % event)
        except ValueError:
            logger.Error("Event not being handled by this instance")
            raise ValueError("Event not being handled by this instance")

    def connect(self, func):
        self.events.add(func)
        logger.debug("Adding event funcCall:: %s" % func)

    def emit(self, *args, **kwargs):
        for event in self.events:
            logger.debug("Calling event :: %s" % event)
            event(*args, **kwargs)
