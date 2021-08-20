
class taskCards:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        
        return self._items

    @property
    def todo_items(self):
        list = []
        for item in self._items:
            if item.status == 'To Do':
                list.append(item)
        return list

    @property
    def doing_items(self):
        list = []
        for item in self._items:
            if item.status == 'Doing':
                list.append(item)
        return list
        


    @property
    def done_items(self):
        list = []
        for item in self._items:
            if item.status == 'Done':
                list.append(item)
        return list
        
    @property
    def should_show_all_done_items(self):
        shouldShow = len(self.done_items) <=3
        return shouldShow

    @property
    def recent_done_items(self):
        list = []
        for item in self.done_items:
            if item.modifiedToday:
                list.append(item)
        return list

        

    @property
    def older_done_items(self):
        list = []
        for item in self.done_items:
            if not item.modifiedToday:
                list.append(item)
        return list
        

