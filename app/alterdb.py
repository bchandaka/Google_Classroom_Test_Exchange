from app import db
from app.models import User, Event, Tournament, Assignment


def del_user(username):
    db.session.delete(User.query.filter_by(username=username).first())
    db.session.commit()


def delete(table, id_start, id_end):
    for i in range(id_start, id_end+1):
        exec("{}.query.filter_by(id={:d}).delete()".format(table, i))
    db.session.commit()


def clear(table):
    exec("{}.query.delete()".format(table))
    db.session.commit()
