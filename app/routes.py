from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from werkzeug.security import generate_password_hash, check_password_hash

from .models import db, User, Question, Answer, Vote
from .forms import LoginForm, RegisterForm, QuestionForm, AnswerForm

main = Blueprint('main', __name__)

# Home page - show all questions
@main.route('/')
def home():
    questions = Question.query.order_by(Question.id.desc()).all()
    return render_template('home.html', questions=questions)

# Register
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username already taken.")
            return redirect(url_for('main.register'))
        user = User(username=form.username.data,
                    password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash("Registered successfully! Please log in.")
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

# Login
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            return redirect(url_for('main.home'))
        flash("Invalid credentials.")
    return render_template('login.html', form=form)

# Logout
@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))

# Ask Question
@main.route('/ask', methods=['GET', 'POST'])
def ask():
    if 'user_id' not in session:
        flash("Please log in to ask.")
        return redirect(url_for('main.login'))
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(title=form.title.data,
                            description=form.description.data,
                            user_id=session['user_id'])
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('ask_question.html', form=form)

# Question Detail + Answer
@main.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question_detail(question_id):
    question = Question.query.get_or_404(question_id)
    answers = Answer.query.filter_by(question_id=question_id).all()
    form = AnswerForm()
    if form.validate_on_submit() and 'user_id' in session:
        answer = Answer(content=form.content.data,
                        question_id=question.id,
                        user_id=session['user_id'])
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('main.question_detail', question_id=question.id))
    return render_template('question_detail.html', question=question, answers=answers, form=form)

# Accept Answer (Only by question owner)
@main.route('/accept/<int:answer_id>/<int:question_id>')
def accept(answer_id, question_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    question = Question.query.get_or_404(question_id)
    if question.user_id == session['user_id']:
        # Un-accept all answers first
        for ans in Answer.query.filter_by(question_id=question_id).all():
            ans.accepted = False
        accepted = Answer.query.get(answer_id)
        accepted.accepted = True
        db.session.commit()
    return redirect(url_for('main.question_detail', question_id=question_id))

# Admin Dashboard
@main.route('/admin')
def admin_dashboard():
    if not session.get('is_admin'):
        return redirect(url_for('main.home'))
    questions = Question.query.all()
    answers = Answer.query.all()
    return render_template('admin_dashboard.html', questions=questions, answers=answers)

# Delete Question (Admin only)
@main.route('/delete/question/<int:question_id>')
def delete_question(question_id):
    if not session.get('is_admin'):
        return redirect(url_for('main.home'))
    question = Question.query.get(question_id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('main.admin_dashboard'))

# Delete Answer (Admin only)
@main.route('/delete/answer/<int:answer_id>')
def delete_answer(answer_id):
    if not session.get('is_admin'):
        return redirect(url_for('main.home'))
    answer = Answer.query.get(answer_id)
    db.session.delete(answer)
    db.session.commit()
    return redirect(url_for('main.admin_dashboard'))
