import gspread
from oauth2client import client
from oauth2client import tools
from oauth2client import file
from app import db
from app.models import User, Event, Tournament
from datetime import datetime
import time
def get_credentials():
    SCOPES = "https://www.googleapis.com/auth/classroom.coursework.students https://www.googleapis.com/auth/classroom.courses https://www.googleapis.com/auth/classroom.push-notifications https://www.googleapis.com/auth/drive https://spreadsheets.google.com/feeds https://www.googleapis.com/auth/classroom.profile.emails"
    store = file.Storage('app/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('app/client_id.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return creds

def start_client():
    creds = get_credentials()
    client = gspread.authorize(creds)
    return client
def load_users(client,filename):
    print('******************Loading Users*********************')
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
def tryoutList(client, filename):
    sheet = client.open(filename).get_worksheet(0)
    all_records = sheet.get_all_records(empty2zero=False,head=1, default_blank='')
    print(all_records)
    print("________________")
    Event_list = ["Anatomy and Physiology","Disease Detectives","Water Quality","Herpetology","Designer Genes","Astronomy","Dynamic Planet","Chemistry Lab", "Forensics","Sounds of Music","Thermodynamics","Mission Possible","Experimental Design","Fermi Questions","Write It Do It","Protein Modeling","Geologic Mapping","Fossils","Boomilever","Circuit Lab","Wright Stuff","Codebusters","Mousetrap Vehicle", ""]
    Event_dict = {}
    for i in Event_list:
        Event_dict[i] = []
    print(Event_dict)
    for i in range(len(all_records)):
        user_name = all_records[i]['First Name'] +" "+ all_records[i]['Last Name']
        print(user_name)
        build_events = all_records[i]["Build/Self-Schedule Events"].split(", ")
        print(build_events)
        if len(build_events)>0:
            for k in build_events:
                Event_dict[k].append(user_name)
        for j in range(6):
            user_events = all_records[i]["Block {}".format(j)].split(", ")
            print(user_events)
            for k in user_events:
                if k != '':
                    print("K is " +k)
                    Event_dict[k].append(user_name)

    print(Event_dict)
    tryoutsheet = client.open("Tryout Check-In").get_worksheet(0)
    for i_num,i in enumerate(Event_dict.keys()):
        tryoutsheet.update_cell(1,i_num+1, i)
        for k_num,k in enumerate(Event_dict[i]):
            tryoutsheet.update_cell(k_num+2,i_num+1, k)
            time.sleep(2)
    tryoutsheet.append_row(Event_dict)

