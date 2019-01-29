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
        print(filename)
        fileDetails = filename.split(',')
        event = fileDetails[1].strip().lower()
        firstname, lastname = fileDetails[0].strip().lower().split()
        origOwner = User.query.filter_by(firstname = firstname.strip(), lastname = lastname.strip()).first()
        tournament_id = 0;
        if Event.query.filter_by(event_name = event,user1_id = origOwner.id).first() is not None:
            eventObj = Event.query.filter_by(event_name = event,user1_id = origOwner.id).first()
            tournament_id = eventObj.tournament_id
        elif Event.query.filter_by(event_name = event,user2_id = origOwner.id).first() is not None:
            eventObj = Event.query.filter_by(event_name = event,user2_id = origOwner.id).first()
            tournament_id = eventObj.tournament_id
        elif Event.query.filter_by(event_name = event,user3_id = origOwner.id).first() is not None:
            eventObj = Event.query.filter_by(event_name = event,user3_id = origOwner.id).first()
            tournament_id = eventObj.tournament_id
        print("Tournament ID: {}".format(tournament_id))
        if(tournament_id != 0):
            partners = find_partners(event, tournament_id)
            for perm in acl:
                #Original File owner
                user = User.query.filter_by(perm_id = perm.get('id')).first()

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
        sendTests(key, assignment,assignment_type, value)




def readPubSub(message):
    try:
        print('***********************Reading Message***********************')

        if message["collection"] == "courses.courseWork":
            if message['eventType'] == "CREATED":
                service = build_service()
                assignment = service.courses().courseWork().get(courseId=message['resourceId']['courseId'], id = message['resourceId']['id']).execute()
                print("Adding new assignment")
                a = Assignment(name = assignment.get('title'), courseWorkId = message['resourceId']['id'])
                db.session.add(a)
                db.session.commit()
        elif message["collection"] == "courses.courseWork.studentSubmissions":
            service = build_service()
            submission = service.courses().courseWork().studentSubmissions().get(courseId=message['resourceId']['courseId'], courseWorkId = message['resourceId']['courseWorkId'], id = message['resourceId']['id']).execute()
            if message['eventType'] == "MODIFIED" and submission['state'] == 'TURNED_IN':
                student=get_student(service, submission["userId"])
                print("Received a submission from ")
                attachments = submission['assignmentSubmission']['attachments']
                errorFiles = []
                for file in attachments:
                    fileTitle = file['driveFile']['title']
                    #File Format: Firstname Lastname, Event, Topic, test/key
                    if re.match(r'^\w+\s\w+\s*,\s*.*,\s*.*,\s*([Tt]est|[Kk]ey)', fileTitle.strip()):
                        fileDetails = fileTitle.split(',')
                        if Event.query.filter_by(event_name=fileDetails[1].strip().lower()).first() != None:
                            print("<b>Filename:</b> " + fileTitle+", <b>Error:</b> None")
                        else:
                            print("<b>Filename:</b> " + fileTitle+", <b>Error:</b> Incorrect Event Name")
                            errorFiles.append("<b>Filename:</b> " + fileTitle+", <b>Error:</b> Incorrect Event Name")
                    else:
                        print("<b>Filename:</b> " +fileTitle+", <b>Error:</b> Incorrect Filename Format")
                        errorFiles.append("<b>Filename:</b> " +fileTitle+", <b>Error:</b> Incorrect Filename Format")
                if errorFiles != []:
                    print("Sending Error Email")
                    #return_work(service,submission["courseId"], submission["courseWorkId"], submission["id"])
                    assignment = Assignment.query.filter_by(courseWorkId=submission['courseWorkId']).first()
                    sendCheckFilename(student["emailAddress"], assignment.name, submission["alternateLink"], errorFiles)
                else:
                    print("Sending Received Submission Email")
                    assignment = Assignment.query.filter_by(courseWorkId=submission['courseWorkId']).first()
                    sendReceivedSubmission(student["emailAddress"], assignment.name, submission["alternateLink"])
            else:
                print("No action on last message")
        else:
            print("No action on last message")
    except Exception as e:
        print("Error reading message:", e)

def pull(project="nv-scioly-manager", subscription_name="receiver"):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project, subscription_name)

    def callback(message):
        print('Received message: {}'.format(message))
        print("Message ID: {}".format(message.message_id))

        update = json.loads(message.data.decode("utf-8"))
        print(update)
        readPubSub(update)

        message.ack()
    future = subscriber.subscribe(subscription_path, callback=callback)

    # The subscriber is non-blocking, so we must keep the main thread from
    # exiting to allow it to process messages in the background.
    print('Listening for messages on {}'.format(subscription_path))
    try:
        # When timeout is unspecified, the result method waits indefinitely.
        future.result(timeout=30)
    except Exception as e:
        print(
          'Listening for messages on {} threw an Exception: {}.'.format(
              subscription_name, e))

#main program captains
"""
clear('Tournament')
clear('Event')

clear('User')

client = start_client()
load_users(client,'Scioly Info Form (Responses)')

load_roster(client,'Huntley 02/09/18')
"""


service = build_service()

#create_registration(service, "Science Olympiad 2018-2019")
test_exchange('Assignment #1', 'Key')

#pull()

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
