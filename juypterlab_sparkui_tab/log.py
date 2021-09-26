import logging
import os


def set_aws_request_id(request_id):
    global aws_request_id
    aws_request_id = request_id


def use_aws_request_id():
    try:
        return aws_request_id
    except:
        return "N/A"


class _Formatter(logging.Formatter):
    def __init__(self, fmt, datefmt, request_id):
        logging.Formatter.__init__(self, fmt, datefmt)
        self.aws_request_id = request_id

    def format(self, record):
        try:
            record.aws_request_id = self.aws_request_id
        except:
            record.aws_request_id = "N/A"

        return super(_Formatter, self).format(record)


def get_logger(class_name):
    logger = logging.getLogger(class_name)
    level =  logging.getLevelName(os.environ.get('loggingLvL', 'DEBUG'))
    logger.setLevel(level)

    root = logging.getLogger()
    root.handlers = []

    for h in logger.handlers:
        logger.removeHandler(h)
    
    # For debugging this module - Writes logs to a file
    #TODO: find a more k8s way to do so
    fh = logging.FileHandler("/tmp/sparkmonitor_serverextension.log", mode="w")
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(levelname)s:  %(asctime)s - %(name)s - %(process)d - %(processName)s - \
        %(thread)d - %(threadName)s\n %(message)s \n")
    fh.setFormatter(formatter)
    logger.addHandler(fh)  ## Comment this line to disable logging to a file.

    # ch = logging.StreamHandler()

    # formatter = _Formatter(
    #     'level=%(levelname)s, timestamp=%(asctime)s, msecs=%(msecs)03d, requestid=%(aws_request_id)s, event=%(module)s.%(funcName)s, msg=%(message)s',
    #     '%Y-%m-%d %H:%M:%S %z',
    #     use_aws_request_id())
    # ch.setFormatter(formatter)
    # logger.addHandler(ch)

    return logger
