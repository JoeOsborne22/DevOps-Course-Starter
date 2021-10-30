
from datetime import datetime,timedelta,date


# attempt at using a claas
class ToDoItem:
    cardsList=[]
    def __init__(self, lists, json):
        self.id = json["id"]
        self.status = lists[json["idList"]]
        self.title = json["name"]
        self.statusId = json["idList"]
        self.due = json["due"]
        self.lastModified = json["dateLastActivity"]
        
        #Set duePast if there is a due date in the past of today
        now=(datetime.now()).date()
        if self.due:
            cardDate=(datetime.fromisoformat(self.due[:-1])).date()
        else:
            #Used when no due date is given, we default to tomorrow so highlight rule is not executed
            cardDate=now + timedelta(days=1)
        self.duePast = now >= cardDate

        #Check if card was last modified today
        lastModDate=(datetime.fromisoformat(self.lastModified[:-1])).date()
        
        self.modifiedToday = lastModDate == now


   