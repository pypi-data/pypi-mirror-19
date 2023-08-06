from django.utils import timezone
import logging


def request_timing_middleware(loghandler, level='INFO'):

    logger = logging.getLogger(loghandler)

    def wrapper(get_response):
        def middleware(request):
            start = timezone.now()
            response = get_response(request)
            finish = timezone.now()
            logger.log(getattr(logging, level), '%s %s %s %s' % (
                start.isoformat(),
                request.method,
                request.path,
                finish - start,
            ))
            return response

        return middleware
    return wrapper
