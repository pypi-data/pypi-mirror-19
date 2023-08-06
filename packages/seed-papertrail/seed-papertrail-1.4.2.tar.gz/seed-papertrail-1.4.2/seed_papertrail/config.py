

def handler(host, port, level='DEBUG',
            handler_class='logging.handlers.SysLogHandler',
            formatter='simple'):
    return {
        'level': level,
        'class': handler_class,
        'formatter': formatter,
        'address': (host, int(port)),
    }


def formatter(sender_name, program_name):
    return {
        'format': '%%(asctime)s %s %s: %%(message)s' % (sender_name,
                                                        program_name),
        'datefmt': '%Y-%m-%dT%H:%M:%S',
    }
