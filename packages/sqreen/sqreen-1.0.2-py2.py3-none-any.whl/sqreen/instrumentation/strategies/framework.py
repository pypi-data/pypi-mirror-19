import sys
import logging

from .import_hook import BaseStrategy
from ..import_hook import ImportHook, get_hook_parent

LOGGER = logging.getLogger(__name__)


class FrameworkStrategy(BaseStrategy):
    """ Specific strategy for framework instrumentation. They hook on atrributes
    defined in the class, MODULE_NAME, HOOK_CLASS, HOOK_METHOD. They wrap the
    resulting object with self.wrapper by passing original as first argument and
    a middleware for the correct framework as second argument
    """

    MODULE_NAME = None
    HOOK_CLASS = None
    HOOK_METHOD = None

    def __init__(self, strategy_key, channel, before_hook_point=None):
        super(FrameworkStrategy, self).__init__(channel, before_hook_point)
        self.strategy_key = strategy_key

        # These values should be defined by subclasses
        self.middleware = None
        self.wrapper = None

    def hook(self):
        """
        Once hooked, the middleware will call the callbacks at the right moment.
        """

        # Check if we already hooked at
        if not self.hooked:

            import_hook = ImportHook(self.MODULE_NAME, self.import_hook_callback)
            sys.meta_path.insert(0, import_hook)

            self.hooked = True

    def import_hook_callback(self, module):
        """ Monkey-patch the object located at hook_class.hook_name on an
        already loaded module
        """
        hook_parent = get_hook_parent(module, self.HOOK_CLASS)

        if hook_parent is None:
            err_msg = "Module {!r} has no attribute {!r}. Module attributes: {}"
            raise AttributeError(err_msg.format(module, self.HOOK_CLASS, dir(module)))

        original = getattr(hook_parent, self.HOOK_METHOD, None)
        hooked = self.wrapper(original, self.middleware)
        setattr(hook_parent, self.HOOK_METHOD, hooked)
        LOGGER.debug("Successfully hooked on %s %s", self.MODULE_NAME,
                     self.HOOK_CLASS)

    @classmethod
    def get_strategy_id(cls, callback):
        """ This strategy only hook on
        (cls.MODULE_NAME::cls.HOOK_CLASS, cls.HOOK_METHOD)
        """
        return ("{}::{}".format(cls.MODULE_NAME, cls.HOOK_CLASS), cls.HOOK_METHOD)

    def _restore(self):
        """ The hooked module will always stay hooked
        """
        pass
