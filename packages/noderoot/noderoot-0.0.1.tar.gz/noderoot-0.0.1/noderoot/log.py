import logging
import logging.handlers
import logging.config
import os
import os.path

def setup(name, path):
    if not os.path.exists(path):
        os.makedirs(path)

    path = "{0}/{1}.log".format(path, name)
    lconfig = dict(
        version = 1,
        formatters = {
            'f': { 'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s' }
            },
        handlers = {
            'c': { 'class': 'logging.StreamHandler',
                   'formatter': 'f',
                   'level': logging.INFO},
            'r': { 'class': 'logging.handlers.RotatingFileHandler',
                   'formatter': 'f',
                   'level': logging.DEBUG,
                   'filename': path,
                   'maxBytes': 102400,
                   'backupCount': 20 }
            },
        root = {
            'handlers': [ 'c', 'r' ],
            'level': logging.DEBUG,
            }
        )

    logging.config.dictConfig(lconfig)

def get(name):
    return logging.getLogger(name)
