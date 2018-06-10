from app import app
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app import db
from app.models import User
from app.forms import LoginForm, SignupForm

@app.route('/index')
def index():
    return render_template('index.html', title = 'NVSO')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        user = User.query.filter_by(email=loginForm.email.data).first()
        if user is None or not user.check_password(loginForm.password.data):
            flash('Invalid usernmae or password')
            return redirect(url_for('login'))
        login_user(user, remember=loginForm.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title = 'Login', form = loginForm)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    signupForm = SignupForm()
    if signupForm.validate_on_submit():
        user = User(firstname=signupForm.firstname.data, lastname=signupForm.lastname.data, email=signupForm.email.data)

        user.set_password(signupForm.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('signup.html', title = 'Login', form = signupForm)
