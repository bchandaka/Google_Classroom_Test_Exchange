from app import db
from app.models import User, Event, Tournament, Assignment
from app.gdrive import *
from app.classroom import *
import re
from app.emailer import *
from app.sheets import *
from google.cloud import pubsub_v1
import time
import json


def find_partners(event, tournament_id):
    eventObj = Event.query.filter_by(event_name=event, tournament_id=tournament_id).first()
    print(eventObj)
    partners = []
    for user_id in [eventObj.user1_id, eventObj.user2_id, eventObj.user3_id]:
        userObj = User.query.filter_by(id=user_id).first()
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
        print(filename)
        fileDetails = filename.split(',')
        event = fileDetails[1].strip().lower()
        firstname, lastname = fileDetails[0].strip().lower().split()
        origOwner = User.query.filter_by(firstname=firstname.strip(), lastname=lastname.strip()).first()
        tournament_id = 0;
        if Event.query.filter_by(event_name=event, user1_id=origOwner.id).first() is not None:
            eventObj = Event.query.filter_by(event_name=event, user1_id=origOwner.id).first()
            tournament_id = eventObj.tournament_id
        elif Event.query.filter_by(event_name=event, user2_id=origOwner.id).first() is not None:
            eventObj = Event.query.filter_by(event_name=event, user2_id=origOwner.id).first()
            tournament_id = eventObj.tournament_id
        elif Event.query.filter_by(event_name=event, user3_id=origOwner.id).first() is not None:
            eventObj = Event.query.filter_by(event_name=event, user3_id=origOwner.id).first()
            tournament_id = eventObj.tournament_id
        print("Tournament ID: {}".format(tournament_id))
        if(tournament_id != 0):
            partners = find_partners(event, tournament_id)
            for perm in acl:
                # Original File owner
                user = User.query.filter_by(perm_id=perm.get('id')).first()

                if user is not None and user in partners:
                    partners.remove(user)
            print(partners)

            for partner in partners:
                if partner is not None:
                    share(service, file.get('id'), partner.email)
                    if partner.email in email_list.keys():
                        email_list[partner.email].append([event, file.get('webViewLink')])
                    else:
                        email_list[partner.email] = []
                        email_list[partner.email].append([event, file.get('webViewLink')])
        else:
            print("{} {} was not found in the roster".format(firstname, lastname))

    print('***********************Sending Emails***********************')
    print(email_list)
    for key, value in email_list.items():
        sendTests(key, assignment, assignment_type, value)

# main program captains


"""
clear('Tournament')
clear('Event')

clear('User')

client = start_client()
load_users(client,'Scioly Info Form (Responses)')

load_roster(client,'Huntley 02/09/18')
"""


service = build_service()

# create_registration(service, "Science Olympiad 2018-2019")
test_exchange('Assignment #1', 'Key')

# pull()

# main program Sample

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
