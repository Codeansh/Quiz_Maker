from werkzeug.wrappers import Request, Response
from pymongo import MongoClient
import jwt

client = MongoClient("localhost:27017")
users = client.quiz_database.user


class Middleware():

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):

        request = Request(environ)
        token = None
        if request.environ.get('REQUEST_URI') in ['/user/login', '/user/register']:
            return self.app(environ, start_response)

        if 'Authorization' in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            msg = 'Please Enter the token to verify your identity...'
            res = Response(msg, mimetype='text/plain', status=401)
            return res(environ, start_response)

        try:
            username = jwt.decode(token, 'This is a secret key', 'HS256')['user_name']

            if not username:
                msg = 'Please Login again '
                res = Response(msg, mimetype='text/plain', status=401)
                return res(environ, start_response)

        except Exception as e:
            msg = 'Something went wrong ' + str(e)
            res = Response(msg, mimetype='text/plain', status=401)
            return res(environ, start_response)

        u = users.find_one({'_id': username})

        if not u:
            msg = 'Username not found  '
            res = Response(msg, mimetype='text/plain', status=401)
            return res(environ, start_response)

        environ['current_user'] = username
        return self.app(environ, start_response)
