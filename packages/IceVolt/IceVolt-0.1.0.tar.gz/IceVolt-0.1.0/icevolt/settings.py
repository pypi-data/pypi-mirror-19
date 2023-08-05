"""Configuration for the application."""

class DevConfig:
    DEBUG = True

class ProdConfig:
    DEBUG = False

class TestConfig:
    DEBUG = True
    TESTING = True
