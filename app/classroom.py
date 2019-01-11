from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
# If modifying these scopes, delete the file token.json.
def get_credentials():
    SCOPES = "https://www.googleapis.com/auth/classroom.coursework.students https://www.googleapis.com/auth/classroom.courses https://www.googleapis.com/auth/classroom.push-notifications https://www.googleapis.com/auth/drive https://spreadsheets.google.com/feeds https://www.googleapis.com/auth/classroom.profile.emails https://www.googleapis.com/auth/classroom.rosters"
    store = file.Storage('app/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('app/client_id.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return creds
def assign_test(service, title, body):
    courseWork = {
                  'title': title,
                  'description': 'Please add your tests/keys with the following naming format: \n Name <Event Name>, Test \n Name <Event Name>, Key \n Ex. Bhargav Chandaka <Write it Do it>, Test \n {}'.format(body),
                  'workType': 'ASSIGNMENT',
                  'state': 'PUBLISHED',
                }
    courseWork = service.courses().courseWork().create(
        courseId='16712128761', body=courseWork).execute()
    print('Assignment created with ID {0}'.format(courseWork.get('id')))
'''
def return_work(service,courseId, courseWorkId, id):
    res = service.courses().courseWork().studentSubmissions()["return"](courseId=courseId, courseWorkId=courseWorkId, id=id).execute()
    return res
'''
def list_courses(service):
    courses = []
    page_token = None

    while True:
        response = service.courses().list(pageToken=page_token,
                                          pageSize=100).execute()
        courses.extend(response.get('courses', []))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            break
    if not courses:
        print("No Courses Found")
    else:
        print('Courses:')
        for course in courses:
            print(u'{0} ({1})'.format(course.get('name'), course.get('id')))
def get_courseId(service, courseName):
    courses = []
    page_token = None
    while True:
        response = service.courses().list(pageToken=page_token,
                                          pageSize=100).execute()
        courses.extend(response.get('courses', []))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            break
    for course in courses:
        if course.get('name') == courseName:
          return course.get('id')
    print("Course Not Found")
    return 18319169120 #default course is Scioly 18/19 course
def create_registration(service,courseName):
    courseId = get_courseId(service,courseName)
    body = {
          "cloudPubsubTopic": {
            "topicName": "projects/nv-scioly-manager/topics/classroomNotify"
          },
          "feed": {
            "feedType": "COURSE_WORK_CHANGES",
            "courseWorkChangesInfo": {
              "courseId": str(courseId)
            }
          }
        }
    response = service.registrations().create(body=body).execute()
    print(response)
def get_student(service,id):
    student = service.userProfiles().get(userId=id).execute()
    return student
def build_service():
    creds = get_credentials()
    service = build('classroom', 'v1', http=creds.authorize(Http()))
    return service

