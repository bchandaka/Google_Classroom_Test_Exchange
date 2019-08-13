from app import db
from app.models import User, Event, Tournament, Assignment
from app.gdrive import *
from app.classroom import *
import re
from app.emailer import *

from google.cloud import pubsub_v1
import time
import json


def pullPubSub(project="nv-scioly-manager", subscription_name="receiver"):
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


def readPubSub(message):
    try:
        print('***********************Reading Message***********************')

        if message["collection"] == "courses.courseWork":
            if message['eventType'] == "CREATED":
                service = build_service()
                assignment = service.courses().courseWork().get(courseId=message['resourceId']['courseId'], id=message['resourceId']['id']).execute()
                print("Adding new assignment")
                a = Assignment(name=assignment.get('title'), courseWorkId=message['resourceId']['id'])
                db.session.add(a)
                db.session.commit()
        elif message["collection"] == "courses.courseWork.studentSubmissions":
            service = build_service()
            submission = service.courses().courseWork().studentSubmissions().get(courseId=message['resourceId']['courseId'], courseWorkId=message['resourceId']['courseWorkId'], id = message['resourceId']['id']).execute()
            if message['eventType'] == "MODIFIED" and submission['state'] == 'TURNED_IN':
                student = get_student(service, submission["userId"])
                print("Received a submission from ")
                attachments = submission['assignmentSubmission']['attachments']
                errorFiles = []
                for file in attachments:
                    fileTitle = file['driveFile']['title']
                    # File Format: Firstname Lastname, Event, Topic, test/key
                    if re.match(r'^\w+\s\w+\s*,\s*.*,\s*.*,\s*([Tt]est|[Kk]ey)', fileTitle.strip()):
                        fileDetails = fileTitle.split(',')

                        if Event.query.filter_by(event_name=fileDetails[1].strip().lower()).first() is not None:
                            print("<b>Filename:</b> " + fileTitle+", <b>Error:</b> None")
                        else:
                            print("<b>Filename:</b> " + fileTitle+", <b>Error:</b> Incorrect Event Name")
                            errorFiles.append("<b>Filename:</b> " + fileTitle+", <b>Error:</b> Incorrect Event Name")
                    else:
                        print("<b>Filename:</b> " + fileTitle + ", <b>Error:</b> Incorrect Filename Format")
                        errorFiles.append("<b>Filename:</b> " + fileTitle + ", <b>Error:</b> Incorrect Filename Format")
                if errorFiles != []:
                    print("Sending Error Email")
                    # return_work(service,submission["courseId"], submission["courseWorkId"], submission["id"])
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
