import json
from datetime import datetime, timedelta

from flask import Blueprint, redirect, render_template, request, url_for, flash

from quiz.authenticate import token_required
from quiz.mquiz.models import Quizes

bp1 = Blueprint('mquiz', __name__, url_prefix='/makeq', template_folder='./templates')


@bp1.route('/create_new', methods=['GET', 'POST'])
@token_required
def create_new(current_user):
    if request.method == 'POST':
        data = json.loads(request.data)
        title = data.get('title')
        description = data.get('description')
        questions = data.get('questions')
        duration = data.get('duration')
        solvers = list(data.get('solvers').split(' '))
        print(solvers)
        print('data', title, questions, description, duration)
        qzs = Quizes(title, current_user, description, questions, datetime.utcnow().strftime("%d %b %Y %l:%M %p"),
                     (datetime.utcnow() + timedelta(hours=int(duration))).strftime("%d %b %Y %l:%M %p"), solvers,
                     duration)
        return Quizes.find_quizes(title)

    return 'Create a quiz'


@bp1.route('/update_quiz/<title>', methods=['GET', 'POST'])
@token_required
def update(current_user, title):
    qzs = Quizes.find_quizes(title)
    if request.method == 'POST':
        quiz = Quizes.find_quizes(title)
        if not quiz:
            return 'Quiz Not Found'
        if not quiz['maker'] != current_user['_id']:
            return 'Action not allowed '

        data = json.loads(request.data)
        description = data.get('description')
        try:
            questions = data.get('questions')

        except:
            return 'Invalid Question'

        duration = data.get('duration')
        solvers = list(data.get('solvers').split(' '))
        Quizes.update(title, description, questions, duration, solvers)
        return Quizes.find_quizes(title)

    return 'Update a quiz'


@bp1.route('view_quizes')
@token_required
def view_quizes(current_user):
    qzs = list(Quizes.find_by_maker(current_user))
    return {'All quizes' : qzs}


@bp1.route('delete_quiz/<title>', methods=['GET'])
@token_required
def delete_quiz(current_user, title):
    qzs = Quizes.find_quizes(title)
    if qzs['maker']['_id'] != current_user['_id']:
        return 'Not allowed to delete'
    Quizes.delete(title)

    return 'Deleted successfully'


@bp1.route('/add_solvers/<title>', methods=['GET', 'POST'])
@token_required
def add_solvers(current_user, title):
    if request.method == 'POST':
        quiz = Quizes.find_quizes(title)
        if not quiz:
            return 'Quiz Not Found'
        if not quiz['maker'] != current_user['_id']:
            return 'Action not allowed '
        solvers = json.loads(request.data).get('solvers')
        Quizes.add_solvers(title, solvers)
        qzs = Quizes.find_quizes(title)
        return {'Solvers Added': qzs}
    return 'Add Solvers'
