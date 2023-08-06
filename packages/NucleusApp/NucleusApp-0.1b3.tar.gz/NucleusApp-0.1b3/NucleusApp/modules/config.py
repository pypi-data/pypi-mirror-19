from NucleusUtils.events import Event

from NucleusApp.app.imports import path_from_module, import_submodules


class AppConfig:
    on_init = Event(name='AppConfig')

    def __init__(self, application, app_name, app_module, submodules):
        self.application = application
        self.name = app_name
        self.module = app_module

        if not hasattr(self, 'label'):
            self.label = app_name.rpartition('.')[2]
        if not hasattr(self, 'path'):
            self.path = path_from_module(app_module)
        self.submodules = submodules
        self.config_module_name = 'app'
        self.configured = False

        self.on_init(self)

    def setup(self):
        self.populate_submodules()
        self.ready()
        self.configured = True

    def populate_submodules(self):
        self.submodules = import_submodules(self.module.__name__, ignore_names=['app', '__init__'])

    def ready(self):
        pass
