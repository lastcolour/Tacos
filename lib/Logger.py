def _createLogger():
    import logging
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")
    return logging.getLogger('main')

Log = _createLogger()
del _createLogger
