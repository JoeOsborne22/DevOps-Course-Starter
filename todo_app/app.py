from operator import attrgetter
from flask import Flask, render_template, request, redirect
from todo_app.flask_config import Config
import os,requests
from dotenv import load_dotenv
from todo_app.ToDoItem  import  ToDoItem

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

#Main functions/app urls

# Main Page - will query for cards and display
@app.route('/')
def index():
    cards=getTrelloCards(trelloBoardID, key, token, False)
    return render_template('index.html',list=cards)

# Used to add new item
@app.route('/add', methods=['POST'])
def add_item():
    card_title=request.form.get('item_name')
    card_desc=request.form.get('item_desc')
    card_due=request.form.get('item_due')
    if not card_title == "": 
        cardDetails={"idList":trelloBaseList,"name":card_title,"pos":"top","desc":card_desc,"due":card_due}
        updateTrelloCard('', cardDetails, "POST", key, token) 
        getTrelloCards(trelloBoardID, key, token, True)   
    return redirect("/")

# Used to sort cards being displayed
@app.route('/sort', methods=['POST'])
def sort_item():
    attr=str(request.form.get('sortBy'))
    if attr == "reset":
        getTrelloCards(trelloBoardID, key, token, True)
        return redirect("/")
    ToDoItem.cardsList=sorted(ToDoItem.cardsList, key=attrgetter(attr))
    return redirect("/")


# used to update the status of an item
@app.route('/mark', methods=['POST'])
def alter_item():
    item=str(request.form.get('item_id'))
    itemId,newState=item.split(";")

    #get valid states/ lists for cards to be in
    trelloLists= {v: k for k, v in getTrelloLists(trelloBoardID, key, token).items()}
    if newState in trelloLists.keys():
        updateTrelloCard(itemId, {"idList":trelloLists[newState]}, "PUT", key, token)
    getTrelloCards(trelloBoardID, key, token, True)        
    return redirect("/")

# Used to delete an item
@app.route('/rem', methods=['POST'])
def remove_item():
    card_id=str(request.form.get('item_id'))
    updateTrelloCard(card_id, {}, "DELETE", key, token)
    getTrelloCards(trelloBoardID, key, token, True)
    return redirect("/")

if __name__ == '__main__':
    app.run()

#Funtions to work with Trello cards
# Used to update an item
def updateTrelloCard (cardId, newState, method, key, token):
    url='https://api.trello.com/1/cards/'+cardId+'?key='+key+'&token='+token
    res=requestJson(method,url, newState)
    return res

    
# Used to get the item cards from a given Trello board
def getTrelloCards(boardId, key, token, refresh):
    if refresh or not ToDoItem.cardsList:
        ToDoItem.cardsList=[]
        trelloLists=getTrelloLists(boardId, key, token)    
        cardDict=getTrelloItems(boardId, 'cards', key, token)
        
        for card in cardDict:
            ToDoItem.cardsList.append(ToDoItem(trelloLists, card))
    return ToDoItem.cardsList

# Used to get the board lists/states from a given Trello board
def getTrelloLists(boardId, key, token):
    listDict=getTrelloItems(boardId, 'lists', key, token)
    listMap={}
    for list in listDict:
        listMap[list["id"]]=list["name"]
    return listMap

# used to get details regarding a boards cards/lists
def getTrelloItems(boardId, item, key, token):
    url='https://api.trello.com/1/boards/'+boardId+'/'+item+'?key='+key+'&token='+token
    res=requestJson("GET",url, {})
    return res
