from .data_interface import *

if "_acive" not in dir():  # Run once
    global _active
    _active = True
    from . import task
