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



