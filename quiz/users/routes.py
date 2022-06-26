import json
import jwt

from flask import Blueprint, redirect, render_template, request, session, url_for, flash

from quiz.authenticate import token_required
from quiz.mquiz.models import Quizes
from quiz.users.models import User

bp2 = Blueprint('user', __name__, url_prefix='/user', template_folder='./templates')


# @bp2.template_filter('to_dict')
# def reverse_filter(s):
#     return json.loads(s)
@bp2.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = json.loads(request.data)
        username = data.get('username')
        fullname = data.get('fullname')
        password = data.get('password')
        email = data.get('email')

        u = User(username, fullname, email)
        u.set_password(password)

        return {'username': u.username, 'email': u.email}
    return 'Please Register'


@bp2.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = json.loads(request.data)
        username = data.get('username')
        password = data.get('password')

        if not username:
            return 'Please Enter A Username'
        if not password:
            return 'Please Enter A Password'
        u = User.get_user(username)

        if not u:
            return "Username doesn't exists"
        check = User.check_password(username, password)
        if check:
            token = jwt.encode({'user_name': username}, 'This is a secret key', algorithm='HS256')
            session['token'] = token
            return {'logged in successfully': token
                    }

        else:
            return 'Please enter correct username and password'
    return {'message':'Please login'}


@bp2.route('/logout')
def logout():
    session.pop('token', None)
    return 'Logout successfully'


@bp2.route('/get_all_quizes')
@token_required
def get_all(current_user):
    qzs = list(User.get_all_quizes(current_user['_id']))
    return {'all quizes':qzs}



@bp2.route('solve_quiz/<title>', methods=['GET', 'POST'])
@token_required
def solve_quiz(current_user, title):
    qz = Quizes.find_quizes(title)
    if not qz:
        return {'error':'Quiz is no longer active'}

    if current_user['_id'] not in qz['solvers']:
        return {'warning': 'You are not allowed to attempt this quiz.'}

    return qz
