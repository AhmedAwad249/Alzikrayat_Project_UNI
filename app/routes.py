def registerRoutes(app):
    """Register Flask listeners --> work to controllers."""

    @app.route("/", methods=["GET"])
    def home():
        from app.controllers.home_controller import HomeController
        return HomeController.index()

    @app.route("/about", methods=["GET"])
    def about():
        """Show the short description of the project."""
        from flask import render_template
        return render_template("about.html")

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


    @app.route("/photos", methods=["GET"])
    def photos():
        from app.controllers.photo_controller import PhotoController
        return PhotoController.index()

    @app.route("/users", methods=["GET"])
    def users():
        """Show the member list."""
        from app.controllers.user_controller import UserController
        return UserController.index()

    @app.route("/user/<int:userId>", methods=["GET"])
    def userProfile(userId):
        """Show a member's public profile."""
        from app.controllers.user_controller import UserController
        return UserController.show(userId)


    @app.route("/photo/upload", methods=["GET"])
    def uploadPhotoForm():
        from app.controllers.photo_controller import PhotoController
        return PhotoController.showUpload()


    @app.route("/photo/store", methods=["POST"])
    def storePhoto():
        from app.controllers.photo_controller import PhotoController
        return PhotoController.store()


    @app.route("/photo/<int:photoId>", methods=["GET"])
    def showPhoto(photoId):
        from app.controllers.photo_controller import PhotoController
        return PhotoController.show(photoId)


    @app.route("/my-photos", methods=["GET"])
    def myPhotos():
        from app.controllers.photo_controller import PhotoController
        return PhotoController.myPhotos()


    @app.route(
        "/photo/<int:photoId>/comment",
        methods=["POST"]
    )
    def storeComment(photoId):
        from app.controllers.comment_controller import CommentController
        return CommentController.store(photoId)


    @app.route(
        "/photo/<int:photoId>/delete",
        methods=["POST"]
    )
    def deletePhoto(photoId):
        from app.controllers.photo_controller import PhotoController
        return PhotoController.delete(photoId)

    @app.route(
    "/photo/<int:photoId>/like",
    methods=["POST"]
    )
    def toggleLike(photoId):
        from app.controllers.like_controller import LikeController
        return LikeController.toggle(photoId)
