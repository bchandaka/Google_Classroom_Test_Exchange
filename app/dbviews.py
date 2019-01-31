from app.models import User, Tournament, Event


def userEvents(tournament, team):
    global Tournament
    t = Tournament.query.filter_by(name=tournament, team=team).first()
    global User
    users = User.query.all()
    global Event
    events = Event.query.filter_by(tournament_id=t.id).all()
    event_dict = {}
    for user in users:
        event_list = []
        for event in events:
            if user.id == event.user1_id or user.id == event.user2_id or user.id == event.user3_id:
                event_list.append(event.event_name)
        event_dict[user.id] = event_list
    return event_dict


t = Tournament.query.filter_by().all()
for tournament in set([tourn.name for tourn in t]):
    for team in set([tourn.team for tourn in t]):
        event_dict = userEvents(tournament, team)
