"""Invoke the application."""
#!/usr/bin/env python3
from .app import create_app


app = create_app()
from . import views
