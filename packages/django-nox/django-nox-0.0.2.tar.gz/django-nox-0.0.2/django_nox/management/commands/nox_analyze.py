from __future__ import absolute_import
from django.core.management.base import BaseCommand
from texttable import Texttable
from django.core.urlresolvers import resolve, Resolver404
from django_nox.models import LoadTimeLog

CACHED_VIEWS = {}


def view_name_from(path):
    try:
        return CACHED_VIEWS[path]

    except KeyError:
        view = resolve(path)
        module = path
        name = ''
        if hasattr(view.func, '__module__'):
            module = resolve(path).func.__module__
        if hasattr(view.func, '__name__'):
            name = resolve(path).func.__name__

        view = "%s.%s" % (module, name)
        CACHED_VIEWS[path] = view
        return view


def generate_table_from(data):
    table = Texttable(max_width=120)
    table.add_row(["view", "method", "status", "count", "query", "minimum", "maximum", "mean", "stdev", "queries", "querytime"])
    table.set_cols_align(["l", "l", "l", "l",  "r", "r", "r", "r", "r", "r", "r"])

    for item in sorted(data):
        mean = round(sum(data[item]['times']) / data[item]['count'], 3)

        mean_sql = round(sum(data[item]['sql']) / data[item]['count'], 3)
        mean_sqltime = round(sum(data[item]['sqltime']) / data[item]['count'], 3)

        sdsq = sum([(i - mean) ** 2 for i in data[item]['times']])
        try:
            stdev = '%.2f' % ((sdsq / (len(data[item]['times']) - 1)) ** .5)
        except ZeroDivisionError:
            stdev = '0.00'

        minimum = "%.2f" % min(data[item]['times'])
        maximum = "%.2f" % max(data[item]['times'])

        table.add_row(
            [data[item]['view'], data[item]['method'], data[item]['status'], data[item]['count'], data[item]['query'],
             minimum, maximum, '%.3f' % mean, stdev, mean_sql, mean_sqltime])

    return table.draw()


def analyze_log(reverse_paths=True):

    data = {}
    rows = LoadTimeLog.objects.all()
    for row in rows:
        date = row.create_time
        method = row.method
        path = row.url
        status = row.code
        time = row.load_time
        sql = row.sql
        sqltime = row.sql_time
        query = row.query

        try:
            if reverse_paths:
                view = view_name_from(path)

            else:
                view = path

            key = "%s-%s-%s-%s" % (view, status, method, query)
            try:
                data[key]['count'] += 1
                data[key]['times'].append(float(time))
                data[key]['sql'].append(int(sql))
                data[key]['sqltime'].append(float(sqltime))
            except KeyError:
                data[key] = {
                    'count': 1,
                    'status': status,
                    'view': view,
                    'method': method,
                    'times': [float(time)],
                    'sql': [int(sql)],
                    'sqltime': [float(sqltime)],
                    'query': query
                }
        except Resolver404:
            pass

    return data


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--reverse',
            dest='reverse',
            action='store_true',
            default=False,
            help='Reverse url for view',
        )

    def handle(self, *args, **options):
        # --date-from YY-MM-DD
        #   specify a date filter start
        #   default to first date in file
        # --date-to YY-MM-DD
        #   specify a date filter end
        #   default to now

        try:
            data = analyze_log(reverse_paths=options.get('reverse', False))
        except Exception:
            import traceback
            traceback.print_exc()
            exit(2)
        else:
            print generate_table_from(data)