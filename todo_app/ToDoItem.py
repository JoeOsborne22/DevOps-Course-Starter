
from datetime import datetime,timedelta


# attempt at using a claas
class ToDoItem:
    cardsList=[]
    def __init__(self, lists, json):
        self.id = json["id"]
        self.status = lists[json["idList"]]
        self.title = json["name"]
        self.statusId = json["idList"]
        self.due = json["due"]
        
        #Set duePast if there is a due date in the past of today
        now=(datetime.now()).date()
        try:
            cardDate=(datetime.fromisoformat(str(json["due"])[:-1])).date()
        except:
            #Used when no due date is given, we default to tomorrow so highlight rule is not executed
            cardDate=now + timedelta(days=1)
        self.duePast = now >= cardDate


   