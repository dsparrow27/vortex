import logging
import logging.handlers
import os
import sys


def getCustomLogger(name='vortex', loglevel='INFO'):
    log = logging.getLogger(name)

    if log.handlers:
        return log
    else:
        loglevel = getattr(logging, loglevel.upper(), logging.INFO)
        log.setLevel(loglevel)

        handler = logging.StreamHandler()
        log.addHandler(handler)

        if log.name == 'root':
            log.warning('Running: %s %s',
                        os.path.basename(sys.argv[0]),
                        ' '.join(sys.argv[1:]))
        return log
