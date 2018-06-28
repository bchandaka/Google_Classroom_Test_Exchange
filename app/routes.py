from app import app
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from wtforms.validators import ValidationError
from app import db
from app.models import User, Event, Tournament
from app.forms import LoginForm, SignupForm
from app.dbviews import userEvents
from datetime import datetime
from app.emailer import *
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

#<-----------------------------Home---------------------------------->
@app.route('/index')
def index():
    return render_template('index.html', title = 'NVScioly Home')

#<---------------------------Signup---------------------------------->
@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    signupForm = SignupForm()
    if signupForm.validate_on_submit():
        user = User(firstname=signupForm.firstname.data, lastname=signupForm.lastname.data,  email=signupForm.email.data, grade = int(signupForm.grade.data), username = signupForm.username.data)
        user.set_password(signupForm.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user! Check Your Email')
        sendSignupEmail(user)
        return redirect(url_for('login'))
    return render_template('signup.html', title = 'Signup', form = signupForm)

#<----------------------------Login---------------------------------->
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        user = User.query.filter_by(username=loginForm.username.data).first()
        if user is None:
            flash('Incorrect Username')
            return redirect(url_for('login'))
        elif not user.check_password(loginForm.password.data):
            flash('Incorrect password')
            return redirect(url_for('login'))
        login_user(user, remember=loginForm.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title = 'Login', form = loginForm)

#<---------------------------Logout---------------------------------->
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#<---------------------------Profile---------------------------------->
@app.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(username=current_user.username).first()
    t = Tournament.query.filter_by().all()
    nameset = set([tourn.name for tourn in t])
    teamset = set([tourn.team for tourn in t])
    event_dict = {}
    return render_template('profile.html', user = user, t = t, teamset= teamset, nameset = nameset, event_dict = event_dict, userEvents = userEvents)
'''
#<----------------------------Admin------------------------------------>
@app.route('/admin')
@login_required
def admin():
    user = User.query.filter_by(username=current_user.username).first()
    if user.admin == True:

    else:
        flash('You do not have access to this section of the site')
        return redirect(url_for('index'))
'''

