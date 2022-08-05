
from datetime import datetime,timedelta,date


# attempt at using a claas
class ToDoItem:
    cardsList=[]
    def __init__(self, json):
        try:
                self.id = json["id"]
        except KeyError:
                self.id = json["_id"]
        self.status = json["idList"]
        self.title = json["name"]
        self.statusId = json["idList"]
        self.due = json["due"]
        self.lastModified = json["dateLastActivity"]
        
        #Set duePast if there is a due date in the past of today
        now=(datetime.now()).date()
        if self.due:
            try:cardDate=(datetime.fromisoformat(self.due[:-1])).date()
            except :cardDate=datetime.strptime(self.due, '%Y-%m-%d').date()
                #cardDate=datetime.combine(datetime.strptime(self.due, '%Y-%m-%d'), datetime.min.time())
        else:
            #Used when no due date is given, we default to tomorrow so highlight rule is not executed
            cardDate=now + timedelta(days=1)
        self.duePast = now >= cardDate

        #Check if card was last modified today
        try:lastModDate=(datetime.fromisoformat(self.lastModified[:-1])).date()
        except:lastModDate=self.lastModified.date()
        
        self.modifiedToday = lastModDate == now


   