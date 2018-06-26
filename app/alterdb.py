from app.admin import *
from app.sheets import *

try:

    clear('User')
    clear('Event')

    # Fake Name Data
    names = sheet.col_values(1)
    for i in names[1:16]:
        add_user(i)
    #Roster Data
    events = sheet.col_values(14)
    user1s = sheet.col_values(15)
    user2s = sheet.col_values(16)
    user3s = sheet.col_values(17)
    for i in range(1,24):
        add_event(events[i], user1s[i], user2s[i], user3s[i])
    mkadmin('bchandaka')
except:
    db.session.rollback()
