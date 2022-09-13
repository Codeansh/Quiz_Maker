import json
import jwt

from flask import Blueprint, request, session, jsonify
from quiz.authenticate import token_required
from quiz.mquiz.models import Quizzes
from quiz.users.models import User
from quiz.users.schemas import NewUser, LoginUser

bp2 = Blueprint('user', __name__, url_prefix='/user', template_folder='./templates')

@bp2.route('/register', methods=['GET', 'POST'])
def register():
    data = json.loads(request.data)
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    data = NewUser(**data)
    u = User.objects(username=username)
    u1 = User.objects(email=email)
    if u:
        return {'message': 'username already registered'}
    if u1:
        return {'message': 'Email already registered'}

    u = User(username=username,email=email,fullname=data.fullname).save()
    u.set_password(password)

    return {'username': u.username, 'email': u.email}


@bp2.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = json.loads(request.data)
        username = data.get('username')
        password = data.get('password')

        data = LoginUser(**data)
        u = User.objects(username=username).first()
        if not u:
            return "Username doesn't exists"
        check = u.check_password(password)
        if check:
            token = jwt.encode({'username': username}, 'This is a secret key', algorithm='HS256')
            session['token'] = token
            return {'logged in successfully': token
                    }

        else:
            return 'Please enter correct username and password'


@bp2.route('/logout')
@token_required
def logout():
    del request.environ['current_user']
    return 'Logout successfully'


@bp2.route('/get_quizzes')

@token_required
def get_all(current_user):
    qzs = Quizzes.objects(maker = current_user.username)
    return jsonify(qzs)



@bp2.route('solve_quiz/<title>', methods=['GET', 'POST'])
@token_required
def solve_quiz(current_user,title:str):

    qz = Quizzes.objects(title=title).first()
    print(qz.solvers)
    if not qz:
        return {'error': 'Quiz is no longer active'}
    if current_user.username not in qz.solvers:
        return {'warning': 'You are not allowed to attempt this quiz.'}

    return qz['questions']
