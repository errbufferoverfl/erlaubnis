# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag

from app import create_app
from config import DebugConfiguration, BaseConfiguration

CONFIG = DebugConfiguration if get_debug_flag() else BaseConfiguration

app = create_app(CONFIG)

if __name__ == '__main__':
    app.run()
