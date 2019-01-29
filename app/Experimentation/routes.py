from app import app
from flask import render_template, request, flash, redirect, url_for

from app import db
from app.models import User, Event, Tournament

from datetime import datetime
from app.emailer import *
from app.gdrive import *


'''
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
'''
#<-----------------------------Home---------------------------------->
@app.route('/index')
def index():
    return render_template('index.html', title = 'NVScioly Home')
'''
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
        credentials = get_credentials()
        if credentials == False or credentials.access_token_expired:
            return redirect(url_for('oauth2callback'))
        else:
            base = create_file('NVScioly-2019', 'application/vnd.google-apps.folder')
            notes = create_file('Notes', 'application/vnd.google-apps.folder', parents = base)
            assignments = create_file('Assignments', 'application/vnd.google-apps.folder', parents = base)
            user_folder = Folders.query.filter_by(user_id=current_user.id).first()
            if  user_folder == None:
                user_folder = Folders(user_id = current_user.id, base_id = base, notes_id = notes, assignments_id = assignments)
                db.session.add(user_folder)
                db.session.commit()
        return redirect(url_for('index'))
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        user = User.query.filter_by(username=loginForm.username.data).first()
        if user is None:
            flash('Incorrect Username')
            return redirect(url_for('login'))
        try:
            if not user.check_password(loginForm.password.data):
                flash('Incorrect password')
                return redirect(url_for('login'))
        except:
            pass
        login_user(user, remember=loginForm.remember_me.data)
        return redirect(url_for('login'))
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
    t = Tournament.query.filter_by().all()
    nameset = set([tourn.name for tourn in t])
    teamset = set([tourn.team for tourn in t])
    event_dict = {}
    return render_template('profile.html', user = current_user, t = t, teamset= teamset, nameset = nameset, event_dict = event_dict, userEvents = userEvents)

#<---------------------------Assignments------------------------------>
@app.route('/assignments')
@login_required
def assignments():
    user_folder = Folders.query.filter_by(user_id=current_user.id).first()
    return render_template('assignments.html', user_folder= user_folder)

@app.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets('app/client_id.json',
            scope='https://www.googleapis.com/auth/drive',
            redirect_uri=url_for('oauth2callback', _external=True)) # access drive api using developer credentials
    flow.params['include_granted_scopes'] = 'true'
    if 'code' not in request.args:
        print('authorizing user')
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        open('app/user_credentials/{}.json'.format(current_user.username),'w+').write(credentials.to_json())
        print('Writing user credentials')# write access token to credentials.json locally
        return redirect(url_for('index'))
'''
#<----------------------------Admin------------------------------------>
@app.route('/admin')
def admin():
    user = User.query.filter_by(username=current_user.username).first()
    if user.admin == True:
        return render_template("admin.html", User=User)
    else:
        flash('You do not have access to this section of the site')
        return redirect(url_for('index'))


