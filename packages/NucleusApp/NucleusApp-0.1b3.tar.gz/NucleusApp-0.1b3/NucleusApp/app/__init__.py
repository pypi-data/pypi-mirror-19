import atexit
import logging
import os
import sys

from NucleusUtils.events import Event
from NucleusUtils.logging.dumps import set_dumps_path
from NucleusUtils.singleton import Singleton

from NucleusApp import VERSION
from NucleusApp.app.log import setup_handlers
from NucleusApp.app.log import setup_level, setup_loggers
from NucleusApp.chest import Chest
from NucleusApp.config import SettingsManager
from NucleusApp.modules.registry import AppsRegistry

APPLICATION = 'app'
SETTINGS = 'settings'
REGISTRY = 'registry'


class Application(metaclass=Singleton):
    """
    Main application Superclass
    """

    # Override this fields in your subclass
    name = ''
    version = VERSION
    settings_module = 'settings'
    modules = [
        'NucleusApp.contrib.logger'
    ]

    # Base application logger
    log = logging.getLogger('NucleusApp')

    def __init__(self):
        self.ready = False

    def run(self):
        """
        You can override this method
        It will be called after loading modules and settings
        :return:
        """
        pass

    @property
    def description(self):
        """
        Get description of application from pydoc
        :return:
        """
        return self.__doc__ or ''

    @description.setter
    def description(self, value):
        self.__doc__ = value

    @property
    def path(self):
        """
        Base application path
        :return:
        """
        return get_base_dir()

    def about(self):
        return "{} v{} - {}".format(self.name, self.version, self.description)

    def setup(self):
        """
        Prepare application for work.
        Load settings and all installed modules
        :return:
        """
        if not self.ready:
            Chest().root[APPLICATION] = self
            Chest().root[SETTINGS] = self.settings
            Chest().root[REGISTRY] = self.registry

            def check_root(name):
                """Prevent to drop app, settings and registry fields"""
                if name == APPLICATION:
                    Chest().root[APPLICATION] = self
                elif name == SETTINGS:
                    Chest().root[SETTINGS] = self.settings
                elif name == REGISTRY:
                    Chest().root[REGISTRY] = self.registry

            Chest().root.on_drop += check_root

            self.settings.load(self.settings_module)
            self.set_logging()
            if not self.registry.ready:
                self.registry.populate(self.modules)

            self.log.debug('Application is loaded!')

            # Trigger on_ready event
            self.ready = True
            self.on_ready.trigger()

            # Call `.run()`
            self.run()

        return self

    def set_logging(self):
        settings = self.settings["LOGGING"]

        setup_level(settings.get('LOG_LEVEL', 'INFO'))
        setup_handlers(settings.get('HANDLERS', []))
        setup_loggers(settings.get('SETUP_LOGGERS', []))
        if settings.get('REPORTS_STORAGE'):
            set_dumps_path(settings.get('REPORTS_STORAGE'))

    def __init_subclass__(cls, **kwargs):
        # Register events
        cls.on_init = Event(name=cls.name + ':on_init')
        cls.on_exit = Event(name=cls.name + ':on_exit')
        cls.on_ready = Event(name=cls.name + ':on_ready')

        # Register SystemExit event
        atexit.register(cls.on_exit)

        # Load settings from settings module
        cls.settings = SettingsManager()

        # Load and populate external modules
        cls.registry = AppsRegistry(cls, None)

        super().__init_subclass__(**kwargs)
        cls.ready = False

        # Trigger on_init event
        cls.on_init()

    def __str__(self):
        return 'Application:' + self.name


def get_base_dir():
    """
    Get base application directory
    :return:
    """
    return os.path.dirname(os.path.abspath(sys.modules.get('__main__').__file__))
