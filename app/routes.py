

def registerRoutes(app):

    @app.route("/", methods=["GET"])
    def home():
        from app.controllers.home_controller import HomeController
        return HomeController.index()