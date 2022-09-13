from flask import Flask, jsonify
from flask_mongoengine import MongoEngine
from quiz.config import Config
from quiz.auth_middleware import Middleware

def create_app():
    app = Flask(__name__)
    # app.wsgi_app = Middleware(app.wsgi_app)
    app.config.from_object(Config)
    app.config['MONGODB_SETTINGS'] = {
        'host': 'mongodb://localhost/quiz_db2'
    }
    db = MongoEngine(app)
    from quiz.mquiz.routes import bp1
    from quiz.users.routes import bp2
    app.register_blueprint(bp1)
    app.register_blueprint(bp2)


    from quiz.mquiz.models import Quizzes
    from quiz.users.models import User
    @app.route("/")
    def root():
        user = User(username = "Shivansh",email ="g@k.com",password ="password").save()

        return jsonify(user), 200


    return app

