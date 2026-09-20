from flask import Flask


def createApp():
    app = Flask(
        __name__,
        template_folder="views/templates"
    )

    from app.routes import registerRoutes
    registerRoutes(app)

    return app