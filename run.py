# -*- coding: utf-8 -*-
"""Create an application instance."""
import os
from typing import Type

from flask.helpers import get_debug_flag

from app import create_app
from config.default import Configuration
from config.dev import DevConfiguration

CONFIG: Type[Configuration]

if get_debug_flag():
    print("Booting Flask app using development configuration.")
    CONFIG = DevConfiguration()
else:
    print("Booting Flask app using development configuration.")
    CONFIG = Configuration()


app = create_app(CONFIG)

if __name__ == '__main__':
    app.run()
