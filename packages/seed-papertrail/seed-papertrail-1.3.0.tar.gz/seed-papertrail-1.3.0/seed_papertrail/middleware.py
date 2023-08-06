from django.utils import timezone
import logging


class RequestTimingMiddleware(object):

    log_handler = 'papertrail'
    log_level = 'INFO'

    def process_request(self, request):
        request._papertrail_start = timezone.now()

    def process_response(self, request, response):
        start = getattr(request, '_papertrail_start')
        if not start:
            return response

        finish = timezone.now()
        logger = logging.getLogger(self.log_handler)
        logger.log(getattr(logging, self.log_level), '%s %s %s %s' % (
            start.isoformat(),
            request.method,
            request.path,
            finish - start,
        ))
        return response


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
