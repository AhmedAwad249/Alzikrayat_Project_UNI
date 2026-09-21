from flask import Flask

from app.config import Config
from app.utils.time_helper import timeAgo


def createApp():
    app = Flask(
        __name__,
        template_folder="views/templates"
    )

    app.config.from_object(Config)

    app.jinja_env.filters["timeAgo"] = timeAgo

    from app.routes import registerRoutes
    registerRoutes(app)

    return app