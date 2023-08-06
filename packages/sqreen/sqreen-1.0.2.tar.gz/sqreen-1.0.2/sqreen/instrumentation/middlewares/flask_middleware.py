# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
from .base import BaseMiddleware


class FlaskMiddleware(BaseMiddleware):
    """ Wrap a RuleCallback and alias its methods to flask middleware methods.
    Nothing connect the failing method to Flask because Flask don't expose any
    way to hook failing middleware like Django.
    """

    def pre(self):
        """ Call wrapped_callback.pre, raise AttackBlock if needed.
        Flask pre callbacks will receive these arguments:
        (None)
        """
        self.strategy.before_hook_point()

        self.execute_pre_callbacks()

    def post(self, response):
        """ Call wrapped_callback.post, raise AttackBlock if needed or returns
        the response passed as input.
        Flask post callbacks will receive these arguments:
        (None, response)
        """
        return self.execute_post_callbacks(response)

    def failing(self, exception):
        """ Call wrapped_callback.failing, always return None.
        Flask failing callbacks will receive these arguments:
        (None, exception)
        """
        self.execute_failing_callbacks(exception)
