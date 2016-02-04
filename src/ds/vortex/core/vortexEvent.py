import logging

logger = logging.getLogger(__name__)


class VortexSignal(object):
    """Custom event signal class, allows you to connect an event to a function or object
    2 main methods that need to be called the first is: connect(funcCall), this adds the arg(func) as a event,
    the second is emit , this is used to trigger the connected events,
    emit(*args, **kwargs) == someFunction(*args, **kwargs)
    example:  myEvent = VortexSignal()
              myEvent.connect(someFunc) # use partial for args
              myEvent.emit(10, "something")
    """

    def __init__(self):
        self.events = set()

    def __len__(self):
        """ the number of events
        :return: int, the number of events
        """
        return len(self.events)

    def removeEvent(self, event):
        """Removes the event instance from the handler
        :param event: function instance
        """
        try:
            self.events.remove(event)
            logger.debug("Removed event:: %s" % event)
        except ValueError:
            logger.Error("Event not being handled by this instance")
            raise ValueError("Event not being handled by this instance")

    def connect(self, func):
        """Create and connect a function to the emit method
        :param func: someFunction instance
        :return: None
        """
        self.events.add(func)
        logger.debug("Adding event funcCall:: %s" % func)

    def hasEvents(self):
        """Checks if object has events
        :return: bool
        """
        if not self.events:
            return False
        return True

    def emit(self, *args, **kwargs):
        """Triggers all the events that have been added, event(*args, **kwargs)
        :param args: arguments to pass to the connected events(functions)
        :param kwargs: dict, same as args
        :return: None
        """

        for event in self.events:
            logger.debug("Calling event :: %s" % event)
            event(*args, **kwargs)
