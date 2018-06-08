from app import app
from flask import render_template, flash, redirect, url_for

from app.forms import LoginForm, SignupForm

@app.route('/index')
def index():
    return render_template('index.html', title = 'NVSO')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        flash('Login requested from user: {}, remember_me: {}'.format(loginForm.email.data, loginForm.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title = 'Login', form = loginForm)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    signupForm = SignupForm()
    if signupForm.validate_on_submit():
        flash('Signup requested from user: {} {}, email: {}'.format(signupForm.firstname.data, signupForm.lastname.data, signupForm.email.data))
        return redirect(url_for('index'))
    return render_template('signup.html', title = 'Login', form = signupForm)
