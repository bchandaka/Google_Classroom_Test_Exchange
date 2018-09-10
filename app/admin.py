from app import db
from app.models import User, Event, Tournament
from app.gdrive import *
import re
from app.emailer import *
from app.sheets import *

def del_user(username):
    db.session.delete(User.query.filter_by(username=username).first())
    db.session.commit()
def delete(table, id_start, id_end):
    for i in range(id_start, id_end+1):
        exec("{}.query.filter_by(id={:d}).delete()".format(table,i))
    db.session.commit()

def clear(table):
    exec("{}.query.delete()".format(table))
    db.session.commit()
def find_partners(event, tournament_id):
    eventObj = Event.query.filter_by(event_name=event, tournament_id= tournament_id).first()
    print(eventObj)
    partners = []
    for user_id in [eventObj.user1_id,eventObj.user2_id, eventObj.user3_id]:
        userObj = User.query.filter_by(id= user_id).first()
        partners.append(userObj)
    return partners

def test_exchange(assignment, assignment_type):
    print('**********************Commencing {} Exchange**************'.format(assignment_type))
    credentials = get_credentials()
    service = build('drive', 'v3', credentials=credentials)
    folder = fetch(service, "name='{}' and mimeType='application/vnd.google-apps.folder'".format(assignment))
    folder_id = folder[0].get('id')

    children = fetch(service, "'{}' in parents and name contains '{}'".format(folder_id, assignment_type))

    email_list = {}
    print('**********************Iterating through Submissions**************')
    for file in children:
        print(file.get('name'))
        acl = fetch_acl(service, file.get('id'))

        filename = file.get('name')
        event = re.search(r'<.*>', filename).group(0).strip('<>').lower()
        partners = find_partners(event, 1)

        for perm in acl:
            #Original File owner
            user = User.query.filter_by(perm_id = perm.get('id')).first()

            if user is not None:
                partners.remove(user)

        for partner in partners:
            if partner is not None:
                share(service, file.get('id'), partner.email)
                if partner.email in email_list.keys():
                    email_list[partner.email].append([event, file.get('webViewLink')])
                else:
                    email_list[partner.email] = []
                    email_list[partner.email].append([event, file.get('webViewLink')])
    print('***********************Sending Emails***********************')
    for key, value in email_list.items():
        sendTests(key, assignment,assignment_type, value)

#main program captains
clear('Tournament')
clear('Event')
clear('User')
client = start_client()
load_users(client,'Captain User data')
load_roster(client,'Captains 08/26/18')
test_exchange('Assignment #2', 'Test')
test_exchange('Assignment #2', 'Key')

#main program Sample

'''
#Share all individual files with fileshare before running code
clear('Tournament')
clear('Event')
clear('User')
client = start_client()
load_users(client,'User data')
load_roster(client,'Test 08/23/18')
test_exchange('Assignment #1', 'Tests')
test_exchange('Assignment #1', 'Keys')
'''
