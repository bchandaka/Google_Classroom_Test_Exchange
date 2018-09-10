import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app import db
from app.models import User, Event, Tournament
from datetime import datetime


def start_client():
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('app/nv-scioly-manager-a7f96a36e7fa.json', scope)
    client = gspread.authorize(creds)
    return client
def load_users(client,filename):
    print('****************Loading Users*********************')
    sheet = client.open(filename).get_worksheet(0)
    firstnames = sheet.col_values(1)
    lastnames = sheet.col_values(2)
    grades = sheet.col_values(3)
    emails = sheet.col_values(4)
    for i in range(1,len(firstnames)):
        add_user(firstnames[i].lower(),lastnames[i].lower(), grades[i],emails[i])

def add_user(firstname, lastname, grade, email):
    user = User(firstname = firstname.strip(), lastname = lastname.strip(), grade = grade.strip(), email = email.strip())
    user.set_perm_id()
    db.session.add(user)
    db.session.commit()
def load_roster(client,filename): #format is 'Tournament Date'
    print('****************Loading Roster*********************')
    tournament, date = filename.lower().split()
    date = datetime.strptime(date, '%m/%d/%y')
    JV = client.open(filename).get_worksheet(1)
    Varsity = client.open(filename).get_worksheet(0)
    for team in [JV, Varsity]:
        add_tournament(date, tournament, team.title.lower())
        events = team.col_values(14)
        user1s = team.col_values(15)
        user2s = team.col_values(16)
        user3s = team.col_values(17)
        for i in range(1,len(events)):
            add_event(tournament, team.title.lower(), events[i].lower(), [user1s[i], user2s[i], user3s[i]])

def add_tournament(date, tournament, team):
    t = Tournament(date=date, name=tournament.strip(), team=team.strip())
    db.session.add(t)
    db.session.commit()

def add_event(tournament, team, event_name, names):
    user_ids = []
    for i in names:
        if i == None or i == '':
            user_ids.append(None)
        else:
            firstname, lastname = i.lower().split()
            u = User.query.filter_by(firstname=firstname, lastname=lastname).first()
            user_ids.append(u.id)
    t = Tournament.query.filter_by(name=tournament, team=team).first()
    event = Event(tournament_id = t.id, event_name = event_name.strip(), user1_id = user_ids[0], user2_id = user_ids[1], user3_id = user_ids[2])
    db.session.add(event)
    db.session.commit()


