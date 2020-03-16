import logging

def _createLogger():
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)] %(message)s")
    return logging.Logger("main")

Log = _createLogger()
