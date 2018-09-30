import sendgrid
import os
from sendgrid.helpers.mail import *
from app.models import User

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
apikey=os.environ.get('SENDGRID_API_KEY')


def sendSignupEmail(user): #parameter is user object
    from_email = Email("bhargav2900@gmail.com")
    subject = "Welcome {}!".format(user.firstname)
    to_email = Email(user.email)
    content = Content("text/html", "This year, the club will be utilizing this website to provide a variety of resources to improve our team's performance. Self made worksheets and tests will be submitted and graded through this site and rosters/other results will be easily available here.")
    mail = Mail(from_email, subject, to_email, content)
    mail.personalizations[0].add_substitution(Substitution("-name-", user.firstname))
    mail.template_id = "5dd8916f-1ed5-43ea-af23-65b5911fd63b"
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

def sendTests(email, assignment,assignment_type, event_list):
    from_email = Email("bhargav2900@gmail.com")
    subject = "{} {}s".format(assignment, assignment_type)
    to_email = Email(email)
    content = Content("text/html", "Good Luck!")
    mail = Mail(from_email, subject, to_email, content)
    user = User.query.filter_by(email=email).first()
    mail.personalizations[0].add_substitution(Substitution("-name-", user.firstname))
    mail.personalizations[0].add_substitution(Substitution("-assignment-", assignment))
    mail.personalizations[0].add_substitution(Substitution("-assignment_type-", assignment_type+'s'))
    eventNum = len(event_list)
    for c in range(eventNum):
        mail.personalizations[0].add_substitution(Substitution("-Event{}name-".format(c+1), event_list[c][0]))
        mail.personalizations[0].add_substitution(Substitution("-Event{}Link-".format(c+1), event_list[c][1]))
    if eventNum == 1:
        mail.template_id = "8238dc2b-2da6-4006-90c4-9129416f9bba"
    elif eventNum == 2:
        mail.template_id = "21ad7fc8-3183-4a77-8509-bb06973f763f"
    elif eventNum == 3:
        mail.template_id = "ad7f080f-bffd-4314-a2ed-da86971b0cfb"
    elif eventNum == 4:
        mail.template_id = "19df88b3-25ef-4a16-bf51-519169cf70ab"

    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

def sendCheckFilename(email, assignment, link, errors):
    from_email = Email("bhargav2900@gmail.com")
    subject = "{} Submission Errors".format(assignment)
    to_email = Email(email)

    content = Content("text/html", "<br/>".join(errors))
    mail = Mail(from_email, subject, to_email, content)
    user = User.query.filter_by(email=email).first()
    mail.personalizations[0].add_substitution(Substitution("-name-", user.firstname))
    mail.personalizations[0].add_substitution(Substitution("-assignmentLink-", link))
    mail.template_id = "c837c4d6-91d8-415a-bbf3-076889b13bd2"
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


