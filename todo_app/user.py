import flask_login

class User(flask_login.UserMixin):

    def __init__(self, id):
        userMap={
            '23385785':"edit",
            '18398852':"edit"
        }
        self.id = id
        self.role = "read"
        if id in userMap:
            self.role = userMap[id]
        

    