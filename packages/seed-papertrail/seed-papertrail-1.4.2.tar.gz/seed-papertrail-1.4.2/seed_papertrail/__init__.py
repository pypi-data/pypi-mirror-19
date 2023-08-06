from .config import handler, formatter


def auto_configure(host, port, system, program, name='papertrail'):
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'papertrail': handler(
                host=host,
                port=int(port), formatter='papertrail')
        },
        'loggers': {
            'papertrail': {
                'handlers': ['papertrail'],
                'level': 'DEBUG',
                'propagate': True,
            }
        },
        'formatters': {
            'papertrail': formatter(system, program)
        }
    }
