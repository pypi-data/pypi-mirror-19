import time
import socket
import resource
from flask import request, g
from flask import _app_ctx_stack as stack
from logging import getLogger
from statsd import StatsClient

log = getLogger(__name__)


def incr(name, value=1):
    _add_metric_to_request('incr', name, value)


def timing(name, value):
    _add_metric_to_request('timing', name, value)


def gauge(name, value):
    _add_metric_to_request('gauge', name, value)


def tag(name, value):
    if not hasattr(g, 'statsd_tags'):
        g.statsd_tags = {}
    g.statsd_tags[name] = value


def _add_metric_to_request(metric_type, metric_name, metric_value):
    if not hasattr(g, 'statsd_metrics'):
        g.statsd_metrics = {
            'timing': [],
            'incr': [],
            'gauge': [],
        }
    assert metric_type in g.statsd_metrics.keys()

    g.statsd_metrics[metric_type].append((metric_name, metric_value))


def add_tags(metric, **tags):
    if not metric:
        return metric
    tag_str = ','.join([('%s=%s' % (k, v)) for k, v in tags.items()])
    return '%s,%s' % (metric, tag_str)


def _get_context_tags():
    try:
        return g.statsd_tags
    except AttributeError:
        return {}


class FlaskStatsdTagged(object):

    def __init__(self, app=None, host='localhost', port=8125, extra_tags={}):
        self.app = app
        self.hostname = socket.gethostname()
        self.statsd_host = host
        self.statsd_port = port
        self.extra_tags = extra_tags
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        app.teardown_request(self.teardown_request)
        self.connection = self.connect()

    def connect(self):
        return StatsClient(host=self.statsd_host,
                           port=self.statsd_port,
                           maxudpsize=1024)

    def before_request(self):
        ctx = stack.top
        ctx.request_begin_at = time.time()
        ctx.resource_before = resource.getrusage(resource.RUSAGE_SELF)
        try:
            ctx.content_length = int(request.headers["content-length"])
        except ValueError:
            ctx.content_length = 0

    def after_request(self, resp):
        ctx = stack.top
        if getattr(ctx, 'statsd_already_executed', False):
            return resp  # This would happen when teardown_request is called after after_request
        ctx.statsd_already_executed = True

        period = (time.time() - ctx.request_begin_at) * 1000
        rusage = resource.getrusage(resource.RUSAGE_SELF)

        tags = dict(self.extra_tags)
        tags.update({"path": request.path or "notfound",
                     "server": self.hostname,
                     "status_code": resp.status_code})
        tags.update(_get_context_tags())
        with self.pipeline() as pipe:
            flaskrequest = add_tags("flaskrequest", **tags)
            pipe.incr(flaskrequest)
            pipe.timing(flaskrequest, period)

            # NOTE: The resource-based timing will (probably) only be relevant if each flask request
            # is handled by a single process, i.e. no threads.

            pipe.timing(add_tags("flask_usertime", **tags), 1000 * (rusage.ru_utime - ctx.resource_before.ru_utime))
            pipe.timing(add_tags("flask_systime", **tags), 1000 * (rusage.ru_stime - ctx.resource_before.ru_stime))

            if ctx.content_length != 0:
                pipe.incr(add_tags("flask_request_datarate", **tags), ctx.content_length)
                pipe.gauge(add_tags("flask_request_datasizegauge", **tags), ctx.content_length)

            self._send_user_metrics(pipe, tags)
        return resp

    @staticmethod
    def _send_user_metrics(pipe, tags):
        metrics = getattr(g, 'statsd_metrics', {})
        for metric_type, metric_names_and_values in metrics.items():
            for metric_name, metric_value in metric_names_and_values:
                getattr(pipe, metric_type)(add_tags(metric_name, **tags), metric_value)

    def teardown_request(self, exception=None):
        # Note that this method is expected to never fail
        class Response500(object):
            status_code = 500
        try:
            self.after_request(Response500())
        except:
            log.exception("Error while tearing down request. "
                          "This has been recovered from but statsd stuff might not have executed.")

    def pipeline(self):
        return self.connection.pipeline()
