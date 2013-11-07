import os
from importlib import import_module

from quizfactory import app
from quizfactory.__main__ import setup

module_name = os.getenv("QUIZFACTORY_SETTINGS", "quizfactory.settings")
module = import_module(module_name)
setup(module)
