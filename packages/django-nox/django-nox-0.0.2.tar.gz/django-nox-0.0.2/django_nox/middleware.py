import time
import logging
import json
from django.db import connection
from django.utils.encoding import smart_str
from django.conf import settings
from models import LoadTimeLog
import django
if django.VERSION[1] >= 10:
    from django.utils.deprecation import MiddlewareMixin
else:
    MiddlewareMixin = object

logger = logging.getLogger(__name__)


class TimeLogMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request._start = time.time()

    def process_response(self, request, response):
        method_map = {
            'GET': request.GET,
            'POST': request.POST,
            'PUT': request.POST,
            'DELETE': request.POST,
            'HEAD': request.POST
        }

        sqltime = 0.0

        for q in connection.queries:
            sqltime += float(q.get('time', 0.0))

        slow_rtime = getattr(settings, "NOX_SLOW_REQUEST", 0)

        if hasattr(request, '_start'):
            d = {
                'method': request.method,
                'load_time': time.time() - request._start,
                'code': response.status_code,
                'url': smart_str(request.path_info),
                'sql': len(connection.queries),
                'sql_time': sqltime,
                'query': json.dumps(method_map[request.method]),
            }

            if logger:
                msg = '%(method)s "%(url)s" (%(code)s) %(load_time).2f (%(sql)dq, %(sql_time).4f)' % d
                logger.info(msg)

            if getattr(settings, "NOX_DB", True):
                if slow_rtime <= d['load_time'] * 1000:
                    LoadTimeLog.objects.create(**d)
        return response
