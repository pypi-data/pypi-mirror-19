import logging

from NucleusUtils.logging.logger import set_level, register_handler, get_logger

from NucleusApp.app.imports import import_attr, split_package


def setup_level(level_name):
    if level_name in ['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'WARN', 'ERROR', 'FATAL', 'CRITICAL']:
        set_level(getattr(logging, level_name))
    else:
        raise KeyError('logging.' + level_name)


def setup_handlers(handlers):
    for handler_settings in handlers:
        handler_module = import_attr(*split_package(handler_settings['HANDLER']))
        handler = handler_module(*handler_settings.get('ARGS') or [], **handler_settings.get('KWARGS') or {})

        formatter_settings = handler_settings.get("FORMATTER")
        if formatter_settings:
            formatter = logging.Formatter(formatter_settings)
            handler.setFormatter(formatter)

        register_handler(handler)


def setup_loggers(loggers_names):
    for name in loggers_names:
        get_logger(name)
