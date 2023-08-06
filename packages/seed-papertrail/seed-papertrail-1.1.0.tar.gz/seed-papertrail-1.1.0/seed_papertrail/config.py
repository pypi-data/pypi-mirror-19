

def handler(host, port, level='DEBUG',
            handler_class='logging.handlers.SysLogHandler',
            formatter='simple'):
    return {
        'level': level,
        'class': handler_class,
        'formatter': formatter,
        'address': (host, int(port)),
    }


def formatter():
    return {
        'format': '%(asctime)s SENDER_NAME PROGRAM_NAME: %(message)s',
        'datefmt': '%Y-%m-%dT%H:%M:%S',
    }
