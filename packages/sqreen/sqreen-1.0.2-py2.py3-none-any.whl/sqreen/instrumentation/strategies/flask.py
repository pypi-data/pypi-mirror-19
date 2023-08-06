# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Flask hook strategy
"""

from logging import getLogger

from .framework import FrameworkStrategy
from ..middlewares import FlaskMiddleware


LOGGER = getLogger(__name__)


def try_trigger_before_first_request_functions_wrapper(original, middleware):

    def wrapped_try_trigger_before_first_request_functions(self, *args, **kwargs):
        LOGGER.debug("Execute try_trigger_before_first_request_functions_wrapper")

        try:
            # Ensure we insert our middleware only once
            if self._got_first_request is False:
                # Insert pre middleware method
                self.before_request_funcs.setdefault(None, []).insert(0, middleware.pre)

                # Insert post middleware method
                self.after_request_funcs.setdefault(None, []).insert(0, middleware.post)
        except Exception:
            LOGGER.warning("Error while inserting our middleware", exc_info=True)

        return original(self, *args, **kwargs)

    return wrapped_try_trigger_before_first_request_functions


class FlaskStrategy(FrameworkStrategy):
    """ Strategy for Flask peripheric callbacks.

    It injects functions that calls pre and post callbacks in the Flask
    request workflow
    """

    MODULE_NAME = "flask.app"
    HOOK_CLASS = "Flask"
    HOOK_METHOD = "try_trigger_before_first_request_functions"

    def __init__(self, strategy_key, channel, before_hook_point=None):
        super(FlaskStrategy, self).__init__(strategy_key, channel, before_hook_point)

        self.middleware = FlaskMiddleware(self, channel)
        self.wrapper = try_trigger_before_first_request_functions_wrapper
