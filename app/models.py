from app import db
from app.gdrive import get_credentials, fetch
from apiclient.discovery import build
import datetime
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(64), index = True)
    lastname = db.Column(db.String(64), index = True)
    email = db.Column(db.String(64), index = True)
    grade = db.Column(db.Integer, index = True)
    perm_id = db.Column(db.String(64), index = True)
    def set_perm_id(self):
        credentials = get_credentials()
        service = build('drive', 'v2', credentials=credentials)
        id_res = service.permissions().getIdForEmail(email=self.email).execute()
        self.perm_id = id_res['id']
    def __repr__(self):
        return '{} {}'.format(self.firstname, self.lastname)
'''
class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, index=True, default=datetime.date.today().strftime("%m/%d/%y"))
    name = db.Column(db.String(64), index = True)
    folder_id = db.Column(db.String(64), index = True)
    def set_folder_id(self,course):
        credentials = get_credentials()
        service = build('drive', 'v3', credentials=credentials)
        folder = fetch("name='{}' and mimeType='application/vnd.google-apps.folder'".format(name))
        self.folder_id = folder[0].get('id')
'''
class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, index=True, default=datetime.date.today().strftime("%m/%d/%y"))
    name = db.Column(db.String(64), index = True)
    team = db.Column(db.String(64), index = True)
    event = db.relationship("Event", backref='event', lazy='dynamic')
    def __repr__(self):
        return('<{} {}>'.format(self.name, self.team))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tournament_id = db.Column(db.String(64), db.ForeignKey('tournament.id'))
    event_name = db.Column(db.String(64), index=True)
    #user ids
    user1_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    user2_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    user3_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    user1 = db.relationship("User", foreign_keys=[user1_id])
    user2 = db.relationship("User", foreign_keys=[user2_id])
    user3 = db.relationship("User", foreign_keys=[user3_id])
    def __repr__(self):
        return('<{} {}>'.format(self.tournament_id, self.event_name))



