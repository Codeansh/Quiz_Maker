
from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for,flash
from quiz.users.models import User
from quiz.mquiz.models import Quizes
import json, jwt
from quiz.authenticate import token_required

bp2 = Blueprint('user',__name__,url_prefix='/user',template_folder='./templates')


# @bp2.template_filter('to_dict')
# def reverse_filter(s):
#     return json.loads(s)
@bp2.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        data = json.loads(request.data)
        username = data.get('username')
        fullname = data.get('fullname')
        password = data.get('password')
        email = data.get('email')

        u = User(username,fullname, email)
        u.set_password(password)

        return {'username':u.username,'email':u.email}
    return 'Please Register'

@bp2.route('/login', methods = ['GET','POST'])
def login():
    message = ''
    if request.method == 'POST':
        # data = json.loads(request.data)
        data = request.form
        username = data.get('username')
        password = data.get('password')

        if not username :
            # return 'Please Enter A Username'
            flash('Please Enter A Username')
            return redirect(url_for('user.login'))

        if not password:
            # return 'Please Enter A Password'
            flash('Please Enter A Password')
            return redirect(url_for('user.login'))
        u = User.get_user(username)

        if not u :
            # return "Username doesn't exists"
            flash("Username doesn't exists")
            return redirect(url_for('user.login'))


        check = User.check_password(username,password)
        if check :
            token = jwt.encode({'user_name':username},'This is a secret key',algorithm='HS256')
            session['token'] = token
            return {'logged in successfully':token
            }
        
        else:
            return 'Please enter correct username and password'
    return render_template('login.html',message=message)

@bp2.route('/logout')
def logout():
    session.pop('token',None)
    return 'Logout successfully'

@bp2.route('/get_all_quizes')
@token_required
def get_all(current_user):
    qzs = (User.get_all_quizes(current_user['_id']))
    print(qzs,current_user)
    return render_template('viewquizes.html',qzs = qzs,user='solver')

@bp2.route('solve_quiz/<title>',methods=['GET','POST'])
@token_required
def solve_quiz(current_user,title):
    qz = Quizes.find_quizes(title)
    if not qz :
        flash('Quiz is no longer active.')
        return redirect(url_for('get_all'))
    if current_user['_id'] not in qz['solvers'] :
        flash('You are not allowed to attempt this quiz.')
        return redirect(url_for('get_all'))
    print(qz['questions'])
    return render_template('solveq.html',qz=qz)