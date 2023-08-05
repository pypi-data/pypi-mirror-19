# -*- coding: utf-8 -*-
import json
import sys
import traceback

from bottle import response
from malibu.util import log


def api_route(path="", actions=[], returns="text/plain"):
    """ decorator api_route(path="", actions=[], returns="text/plain")

        Sets values on route functions to automate
        loading routes into Bottle.
    """

    def api_route_outer(route_function):

        pre_execs = []

        if returns:
            def _set_return_type():
                response.content_type = returns

            pre_execs.append(_set_return_type)

        setattr(route_function, "route_func", True)
        setattr(route_function, "path", path)
        setattr(route_function, "actions", actions)
        setattr(route_function, "pre_exec", pre_execs)

        return route_function

    return api_route_outer


def json_response(route_function):
    """ decorator json_response(route_function)

        Takes the return value from a route and dumps it to a JSON string.
    """

    _LOG = log.LoggingDriver.find_logger()

    def _json_resp_inner(*args, **kw):

        if response.content_type is not "application/json":
            response.content_type = "application/json"

        try:
            resp = route_function(*args, **kw)
        except Exception as e:
            raise e

        if isinstance(resp, str):
            _LOG.warning(
                '@json_response is applied to route but a string was '
                'returned.'
            )
            return resp

        try:
            return json.dumps(resp)
        except:
            return resp

    return _json_resp_inner


def status_returned(route_function):
    """ decorator status_returned()

        Indicates that a status code was returned with the response.
        Try to find it and set the bottle global response object's status
        code accordingly.
    """

    _LOG = log.LoggingDriver.find_logger()

    def _status_ret_inner(*args, **kw):

        try:
            resp = route_function(*args, **kw)
        except Exception as e:
            raise e

        if not isinstance(resp, dict):
            _LOG.warning(
                '@status_returned is applied to route but a dict was '
                'not returned.'
            )
            return resp

        if isinstance(resp.get('status', None), int):
            response.status = resp.get('status')
            return resp
        else:
            _LOG.warning(
                '@status_returned is applied to route but no [status] '
                'key was found in response.'
            )
            return resp

    return _status_ret_inner


class APIRouter(object):

    def __init__(self, manager):

        self._log = log.LoggingDriver.find_logger()

        self.manager = manager
        self.app = self.manager.app

        self.routes = self.load_routes()

    def load_routes(self):
        """ load_routes(self)

            Loads route functions into Bottle based on the presence of
            extra variables in a function object.
        """

        routes = []

        for member in dir(self):
            member = getattr(self, member)
            if member and hasattr(member, "route_func"):
                self._log.debug(
                    "Found routing function %s" % (member.__name__)
                )
                routes.append(member)

        for route in routes:
            self._log.debug("Routing %s requests to %s for path -> %s" % (
                route.actions, route.__name__, route.path))
            if route.pre_exec:
                def _pe_wrap(r):
                    route_handler = r

                    def _pe_internal(*args, **kw):
                        try:
                            [pef() for pef in route_handler.pre_exec]
                        except Exception:
                            self.manager.dsn.client.captureException()

                        return route_handler(*args, **kw)
                    return _pe_internal

                self.app.route(route.path, route.actions, _pe_wrap(route))
            else:
                self.app.route(route.path, route.actions, route)

        return routes

    def generate_bare_response(self):
        """ generate_bare_response()

            Generates a bare, generic "good" response.
        """

        response = {"status": 200}

        return response

    def generate_error_response(self, code=500, exception=None, debug=False):
        """ generate_error_response(code=500, exception=None, debug=False)

            Generates a dictionary with error codes and exception information
            to return instead of a bland, empty dictionary.

            The `code` parameter will set the status code in the response. If
            not provided, it defaults to 500.

            If exception is not provided, this method will return exception
            information based on the contents of sys.last_traceback
        """

        response = {"status": code}

        if debug:
            response.update({"stacktrace": {}})
            traceback_pos = 0
            for trace in traceback.extract_tb(sys.exc_info()[2], 4):
                response['stacktrace'].update({
                    str(traceback_pos): ' '.join(trace)
                })
                traceback_pos += 1

        if exception:
            response.update({"exception": str(exception)})

        return response
