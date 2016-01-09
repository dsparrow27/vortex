import logging
import logging.handlers
import os
import sys


def getCustomLogger(name='vortex', loglevel='INFO'):
    log = logging.getLogger(name)

    # if logger 'name' already exists, return it to avoid logging duplicate
    # messages by attaching multiple handlers of the same type
    if log.handlers:
        return log
    # if logger 'name' does not already exist, create it and attach handlers
    else:
        # set logLevel to loglevel or to INFO if requested level is incorrect
        loglevel = getattr(logging, loglevel.upper(), logging.INFO)
        log.setLevel(loglevel)

        handler = logging.StreamHandler()
        log.addHandler(handler)

        if log.name == 'root':
            log.warning('Running: %s %s',
                        os.path.basename(sys.argv[0]),
                        ' '.join(sys.argv[1:]))
        return log
