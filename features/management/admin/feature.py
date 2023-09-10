import logging
from . import config_report
from . import set_role
from . import settings
from . import youtube

_logger = logging.getLogger("main")


if "_acive" not in dir():  # Run once
    global _active
    _active = False


def is_active():
    return _active


def activate():
    global _active
    _active = True
    _logger.debug("features: Feature has been activated: 'management/admin'")
    config_report.activate()
    set_role.activate()
    settings.activate()
    youtube.activate()
