import logging

FORMAT = '%(asctime)s %(name)-12s %(levelname)s : %(message)s'
#logging.basicConfig(level=logging.DEBUG, format=FORMAT)


def logging_init(s):
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    log = logging.getLogger(s)
    #log.basicConfig(level=logging.DEBUG, format=FORMAT)
    return log