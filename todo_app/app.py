from operator import itemgetter
from flask import Flask, render_template, request, redirect
from todo_app.data import session_items
from todo_app.flask_config import Config
import os, requests, json
from dotenv import load_dotenv

# Set app variables
load_dotenv()
key=os.getenv('TRELLO_KEY')
token=os.getenv('TRELLO_TOKEN')
trelloBoardID='60fad7c6c463fc540fbffb94'
trelloBaseList='60fad7c6c463fc540fbffb95' # will place new cards in To Do list
app = Flask(__name__)
app.config.from_object(Config)

# Dictionary used to map request calls 
jsonDict={
    "PUT":requests.put,
    "POST":requests.post,
    "GET":requests.get,
    "DELETE":requests.delete
}

# Common function used to request data from URL's
def requestJson (method, url, args):
    r = jsonDict[method](url, params=args) 
    r.raise_for_status()
    #Should handle error statuses - TODO
    return r.json()


# Main Page - will query for cards and display
@app.route('/')
def index():
    cards=getTrelloCards(trelloBoardID)
    return render_template('index.html',list=cards)

# Used to add new item
@app.route('/add', methods=['POST'])
def add_item():
    user_item=request.form.get('item_name')
    if not user_item == "": 
        cardDetails={"idList":trelloBaseList,"name":user_item,"pos":"top"}
        updateTrelloCard('', cardDetails, "POST")    
    return redirect("/")

# used to update the status of an item
@app.route('/mark', methods=['POST'])
def alter_item():
    item=str(request.form.get('item_id'))
    itemId,newState=item.split(";")

    #get valid states/ lists for cards to be in
    trelloLists= {v: k for k, v in getTrelloLists(trelloBoardID).items()}
    if newState in trelloLists.keys():
        updateTrelloCard(itemId, {"idList":trelloLists[newState]}, "PUT")
    return redirect("/")

# Used to delete an item
@app.route('/rem', methods=['POST'])
def remove_item():
    card_id=str(request.form.get('item_id'))
    updateTrelloCard(card_id, {}, "DELETE")
    return redirect("/")

# Used to get the item cards from a given Trello board
def getTrelloCards(boardId):
    res=[]
    cardDict=getTrelloItems(boardId, 'cards')
    trelloLists=getTrelloLists(boardId)
    
    for card in cardDict:
        cardDetails={"id":card["id"],"list":card["idList"],"title":card["name"],"status":trelloLists[card["idList"]]}
        res.append(cardDetails)
    
    return res

# Used to get the board lists/states from a given Trello board
def getTrelloLists(boardId):
    listDict=getTrelloItems(boardId, 'lists')
    listMap={}
    for list in listDict:
        listMap[list["id"]]=list["name"]
    return listMap

# used to get details regarding a boards cards/lists
def getTrelloItems(boardId, item):
    url='https://api.trello.com/1/boards/'+boardId+'/'+item+'?key='+key+'&token='+token
    res=requestJson("GET",url, {})
    return res

# Used to update an item
def updateTrelloCard (cardId, newState, method):
    url='https://api.trello.com/1/cards/'+cardId+'?key='+key+'&token='+token
    res=requestJson(method,url, newState)
    return res


if __name__ == '__main__':
    app.run()


# attempt at using a claas
class ToDoItem:
    def __init__(self, id, status, title, statusId):
        self.id = id
        self.status = status
        self.title = title
        self.statusId = statusId

