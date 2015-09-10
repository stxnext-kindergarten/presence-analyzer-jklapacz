# -*- coding: utf-8 -*-
"""
Flask app initialization.
"""
import os.path
from flask import Flask

app = Flask(__name__)  # pylint: disable=invalid-name
app.config.update(
    DEBUG=True
)
