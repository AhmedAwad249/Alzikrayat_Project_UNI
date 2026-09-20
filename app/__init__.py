from flask import Flask

from app.config import Config


def createApp():
    """Create and configure the Flask application."""

    app = Flask(
        __name__,
        template_folder="views/templates"
    )

    app.config.from_object(Config)
    

    from app.routes import registerRoutes
    registerRoutes(app)

    return app