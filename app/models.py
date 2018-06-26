from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
import datetime
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(64), index = True)
    lastname = db.Column(db.String(64), index = True)
    email = db.Column(db.String(64), index = True)
    grade = db.Column(db.Integer, index = True)
    username = db.Column(db.String, index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    admin = db.Column(db.Boolean, default=False, index=True)
    def __repr__(self):
        return('<User {}>'.format(self.username))
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password_hash, password)
    def fullname(self):
        return '{} {}'.format(self.firstname, self.lastname)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, index=True, default=datetime.date.today().strftime("%m/%d/%y"))
    tournament = db.Column(db.String(64), index = True)
    team = db.Column(db.String(64), index = True)
    event_name = db.Column(db.String(64), index = True)
    #user ids
    user1_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    user2_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    user3_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    user = db.relationship("User", foreign_keys = [user1_id])
    def __repr__(self):
        return('<{} {}>'.format(self.tournament, self.event))
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

