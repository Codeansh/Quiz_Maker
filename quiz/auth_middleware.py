from werkzeug.wrappers import Request, Response
import jwt
from quiz.users.models import User
class Middleware():
    def __init__(self, app):
        self.app = app
        self.username = 'shiv'
        self.password = 'shiv'
    def __call__(self, environ, start_response):

        request = Request(environ)
        token = None

        if 'Authorization' in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
            print(token)
        if not token:
            msg = 'Please Enter the token to verify your identity...'
            res = Response(msg, mimetype='text/plain', status=401)
            return res(environ, start_response)

        try:
            username = jwt.decode(token, 'This is a secret key', 'HS256')['user_name']
            current_user = User.get_user(username)

            if not current_user:
                msg = 'Please Login again '
                res = Response(msg, mimetype='text/plain', status=401)
                return res(environ, start_response)

        except Exception as e:
            msg = 'Something went wrong '+ str(e)
            res = Response(msg, mimetype='text/plain', status=401)
            return res(environ, start_response)

        environ['current_user'] = current_user
        return self.app(environ, start_response)


