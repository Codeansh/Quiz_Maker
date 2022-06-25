from crypt import methods
from ctypes import resize
from pydoc import render_doc
from flask import Blueprint, redirect, render_template, request, jsonify, url_for, flash
from quiz.mquiz.models import Quizes
from datetime import datetime, timedelta
import json
from quiz.authenticate import token_required

bp1 = Blueprint('mquiz',__name__,url_prefix='/makeq',template_folder='./templates')

@bp1.route('/create_new', methods=['GET','POST'])
@token_required
def create_new(current_user):

    if request.method == 'POST':
        # data = json.loads(request.data)
        data = request.form
        title = data.get('title')
        description = data.get('description')
        print(data.get('questions'))
        questions = json.loads(data.get('questions').replace("'",'"'))
        duration = data.get('duration')
        solvers =list(data.get('solvers').split(' '))
        print(solvers)
        print('data',title,questions,description,duration)
        Quizes(title,current_user,description,questions,datetime.utcnow().strftime("%d %b %Y %l:%M %p"),(datetime.utcnow()+timedelta(hours=int(duration))).strftime("%d %b %Y %l:%M %p"),solvers,duration)
        return redirect(url_for('mquiz.view_quizes'))
    # return 'Create a quiz'
    return render_template('create.html',qzs=None)

@bp1.route('/update_quiz/<title>', methods=['GET','POST'])
@token_required
def update(current_user,title):
    qzs = Quizes.find_quizes(title)
    if request.method == 'POST':
        # data = json.loads(request.data)
        quiz = Quizes.find_quizes(title)
        if not quiz :
            return 'Quiz Not Found'
        if not quiz['maker'] != current_user['_id'] :
            return 'Action not allowed '
        data = request.form
        description = data.get('description')
        try :
            questions = json.loads(data.get('questions').replace("'",'"'))
        except:
            flash('Invalid Question')
            return render_template('create.html',qzs=qzs)
        print(data.get('questions'),type(questions),questions)
        duration = data.get('duration')
        solvers =list(data.get('solvers').split(' '))
        Quizes.update(title,description,questions,duration,solvers)
        return redirect(url_for('mquiz.view_quizes'))
    # return 'Create a quiz'

    return render_template('create.html',qzs=qzs)

@bp1.route('view_quizes')
@token_required
def view_quizes(current_user):
    qzs = Quizes.find_by_maker(current_user)
    return render_template('view_quizes.html',qzs = qzs)

@bp1.route('delete_quiz/<title>',methods=['GET'])
@token_required
def delete_quiz(current_user,title):
    qzs = Quizes.find_quizes(title)
    print(qzs,current_user)
    if qzs['maker']['_id'] != current_user['_id']:
        flash('Not allowed to delete.')
        return redirect(url_for('mquiz.view_quizes'))
    Quizes.delete(title)

    return redirect(url_for('mquiz.view_quizes'))




@bp1.route('/add_solvers/<title>',methods=['GET','POST'])
@token_required
def add_solvers(current_user,title):
    if request.method == 'POST':
        quiz = Quizes.find_quizes(title)
        if not quiz :
            return 'Quiz Not Found'
        if not quiz['maker'] != current_user['_id'] :
            return 'Action not allowed '
        solvers = json.loads(request.data).get('solvers')
        Quizes.add_solvers(title,solvers)
        return 'Solvers Added'
    return 'Add Solvers'





