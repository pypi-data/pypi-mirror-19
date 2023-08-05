"""Application factories."""
from .settings import DevConfig
from flask import Flask


def create_app(config=DevConfig):
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config)
    return app
