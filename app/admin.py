from app import db
from app.models import User, Event, Tournament

def delete(table, id_start, id_end):
    for i in range(id_start, id_end+1):
        exec("{}.query.filter_by(id={:d}).delete()".format(table,i))
    db.session.commit()

def clear(table):
    exec("{}.query.delete()".format(table))
    db.session.commit()

def mkadmin(username):
    u = User.query.filter_by(username=username).first()
    u.admin = True
    db.session.commit()


