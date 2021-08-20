from todo_app.app import app
from todo_app.viewModel import taskCards
from todo_app.ToDoItem  import  ToDoItem
import pytest 

from datetime import datetime


statusList = ['To Do','Doing','Done','Test']

def test_items_category_split():
	items = [
		ToDoItem(statusList,{'id':1, 'idList':0,'name':'task 1','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':"2021-08-20T00:00:00.000Z"}),
		ToDoItem(statusList,{'id':2, 'idList':1,'name':'task 2','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':"2021-08-20T00:00:00.000Z"}),
		ToDoItem(statusList,{'id':3, 'idList':2,'name':'task 3','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':"2021-08-20T00:00:00.000Z"}),
		ToDoItem(statusList,{'id':4, 'idList':3,'name':'task 4','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':"2021-08-20T00:00:00.000Z"}),
		ToDoItem(statusList,{'id':5, 'idList':2,'name':'task 5','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':"2021-08-20T00:00:00.000Z"}),
		ToDoItem(statusList,{'id':6, 'idList':1,'name':'task 6','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':"2021-08-20T00:00:00.000Z"})
	]	

	view = taskCards(items)
	
	todo_items_tasks=[]
	for card in view.todo_items:
    		todo_items_tasks.append(card.title)
	assert todo_items_tasks == ['task 1']

	doing_items_tasks=[]
	for card in view.doing_items:
    		doing_items_tasks.append(card.title)
	assert doing_items_tasks == ['task 2','task 6']

	done_items_tasks=[]
	for card in view.done_items:
    		done_items_tasks.append(card.title)
	assert done_items_tasks == ['task 3','task 5']


def test_no_matching_status():
    
    items = [ToDoItem(statusList,{'id':1, 'idList':3,'name':'task 1','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':"2021-08-20T00:00:00.000Z"})]
    view = taskCards(items)
    assert len(view.todo_items) == 0
    assert len(view.doing_items) == 0
    assert len(view.done_items) == 0

def test_show_all_done():
	items = [
		ToDoItem(statusList,{'id':1, 'idList':0,'name':'task 1','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':"2021-08-20T00:00:00.000Z"}),
		ToDoItem(statusList,{'id':2, 'idList':1,'name':'task 2','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':"2021-08-20T00:00:00.000Z"}),
		ToDoItem(statusList,{'id':3, 'idList':2,'name':'task 3','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':"2021-08-20T00:00:00.000Z"}),
		ToDoItem(statusList,{'id':5, 'idList':2,'name':'task 5','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':"2021-08-20T00:00:00.000Z"})
	]	
	view = taskCards(items)
	assert view.should_show_all_done_items is True


def test_not_show_all_done_if_more_than_three():
	items = [
		ToDoItem(statusList,{'id':1, 'idList':0,'name':'task 1','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':"2021-08-20T00:00:00.000Z"}),
		ToDoItem(statusList,{'id':2, 'idList':1,'name':'task 2','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':"2021-08-20T00:00:00.000Z"}),
		ToDoItem(statusList,{'id':3, 'idList':2,'name':'task 3','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':"2021-08-20T00:00:00.000Z"}),
		ToDoItem(statusList,{'id':5, 'idList':2,'name':'task 5','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':"2021-08-20T00:00:00.000Z"}),
		ToDoItem(statusList,{'id':5, 'idList':2,'name':'task 5','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':"2021-08-20T00:00:00.000Z"}),
		ToDoItem(statusList,{'id':5, 'idList':2,'name':'task 5','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':"2021-08-20T00:00:00.000Z"})
	]	
	view = taskCards(items)
	assert view.should_show_all_done_items is False


def test_recent_done_items_done_today():
	now = datetime.now()
	dt_string = str(now.strftime("%Y-%m-%d"))
	active=dt_string+"T00:00:00.000Z"
	items = [
		ToDoItem(statusList,{'id':3, 'idList':2,'name':'task 3','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':active}),
		ToDoItem(statusList,{'id':4, 'idList':2,'name':'task 4','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':"2021-08-19T00:00:00.000Z"}),
		ToDoItem(statusList,{'id':5, 'idList':1,'name':'task 5','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':active}),
		ToDoItem(statusList,{'id':6, 'idList':0,'name':'task 6','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':active})
	]	
	view = taskCards(items)
	#Extract the id's of our objects for comparison
	recentDone = []
	for item in view.recent_done_items:
		recentDone.append(item.id)
	check = [3]
	assert recentDone == check	

def test_older_done_items_no_items_today():
	now = datetime.now()
	dt_string = str(now.strftime("%Y-%m-%d"))
	active=dt_string+"T00:00:00.000Z"
	items = [
		ToDoItem(statusList,{'id':3, 'idList':2,'name':'task 3','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':active}),
		ToDoItem(statusList,{'id':4, 'idList':2,'name':'task 4','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':"2021-08-19T00:00:00.000Z"}),
		ToDoItem(statusList,{'id':5, 'idList':1,'name':'task 5','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':active}),
		ToDoItem(statusList,{'id':6, 'idList':0,'name':'task 6','due':"2021-08-27T00:00:00.000Z",'dateLastActivity':active})
	]	
	view = taskCards(items)
	#Extract the id's of our objects for comparison
	recentDone = []
	for item in view.older_done_items:
		recentDone.append(item.id)
	check = [4]
	assert recentDone == check	
