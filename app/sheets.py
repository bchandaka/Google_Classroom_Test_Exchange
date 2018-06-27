import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app import db
from app.models import User, Event, Tournament
import datetime
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
tournament = 'State'
date = datetime.date(2018,5,28)
sheet = client.open('{} {}'.format(tournament, date)).get_worksheet(1)
team = sheet.title
def add_user(name):
    firstname, lastname = name.split()
    username = firstname[0] + lastname
    email = 'bhargav2900@gmail.com'
    password = 'abc' # same password for all fake users
    grade = 10
    a = User(firstname = firstname, lastname = lastname, grade = grade, email = email, username = username.lower())
    a.set_password(password)
    db.session.add(a)
    db.session.commit()
def add_tournament():
    global date
    global tournament
    global team
    t = Tournament(date=date, name=tournament, team=team)
    db.session.add(t)
    db.session.commit()
def add_event(event_name, name1, name2, name3):
    user_ids = []
    for i in [name1,name2,name3]:
        if i != '':
            firstname, lastname = i.split()
            u = User.query.filter_by(firstname=firstname, lastname=lastname).first()
            user_ids.append(u.id)
        else:
            user_ids.append(None)
    global tournament
    global team
    t = Tournament.query.filter_by(name=tournament, team=team).first()
    event = Event(tournament_id = t.id, event_name = event_name, user1_id = user_ids[0], user2_id = user_ids[1], user3_id = user_ids[2])
    db.session.add(event)
    db.session.commit()


