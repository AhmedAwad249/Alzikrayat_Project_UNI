def registerRoutes(app):
    """Register Flask listeners --> work to controllers."""

    @app.route("/", methods=["GET"])
    def home():
        from app.controllers.home_controller import HomeController
        return HomeController.index()

    @app.route("/register", methods=["GET"])
    def registerForm():
        from app.controllers.auth_controller import AuthController
        return AuthController.showRegister()

    @app.route("/register", methods=["POST"])
    def registerUser():
        from app.controllers.auth_controller import AuthController
        return AuthController.register()

    @app.route("/login", methods=["GET"])
    def loginForm():
        from app.controllers.auth_controller import AuthController
        return AuthController.showLogin()

    @app.route("/login", methods=["POST"])
    def loginUser():
        from app.controllers.auth_controller import AuthController
        return AuthController.login()

    @app.route("/logout", methods=["POST"])
    def logoutUser():
        from app.controllers.auth_controller import AuthController
        return AuthController.logout()