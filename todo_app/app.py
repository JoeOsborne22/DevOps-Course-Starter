from operator import attrgetter
from todo_app.viewModel import taskCards
from flask import Flask, render_template, request, redirect, session
import os,requests
from todo_app.ToDoItem  import  ToDoItem
#from todo_app.createApp import createApp


# Common function used to request data from URL's
def requestJson (method, url, args):
    r = requests.request(method, url, params=args) 
    r.raise_for_status()
    print(r.raise_for_status())
    #Should handle error statuses - TODO
    return r.json()

def create_app():
    app = Flask(__name__)
    app.secret_key=os.getenv('TODO_APP_SECRET_KEY')

    # Set app variables
    key=os.getenv('TRELLO_KEY')
    token=os.getenv('TRELLO_TOKEN')
    trelloBoardID=os.getenv('TRELLO_BOARD_ID')
    trelloBaseList=os.getenv('TRELLO_BASE_LIST') # will place new cards in To Do list

    #Main functions/app urls
    # Main Page - will query for cards and display
    @app.route('/')
    def index():
        cards=getTrelloCards(trelloBoardID, key, token)
        if "sortAttr" in session:
            cards=sorted(cards, key=attrgetter(session.get('sortAttr')))
        item_view_model= taskCards(cards)
        return render_template('index.html',viewModel=item_view_model)

    # Used to add new item
    @app.route('/add', methods=['POST'])
    def add_item():
        card_title=request.form.get('item_name')
        card_desc=request.form.get('item_desc')
        card_due=request.form.get('item_due')
        if not card_title == "": 
            cardDetails={"idList":trelloBaseList,"name":card_title,"pos":"top","desc":card_desc,"due":card_due}
            updateTrelloCard('', cardDetails, "POST", key, token) 
        return redirect("/")

    # Used to sort cards being displayed
    @app.route('/sort', methods=['POST'])
    def sort_item():
        attr=str(request.form.get('sortBy'))
        session['sortAttr']=attr
        if attr == "reset":
            session.pop('sortAttr')     
        return redirect("/")


    # used to update the status of an item
    @app.route('/mark', methods=['POST'])
    def alter_item():
        newState=str(request.form.get('item_state'))
        itemId=str(request.form.get('item_id'))

        #get valid states/ lists for cards to be in
        trelloLists= {v: k for k, v in getTrelloLists(trelloBoardID, key, token).items()}
        if newState in trelloLists.keys():
            updateTrelloCard(itemId, {"idList":trelloLists[newState]}, "PUT", key, token)
        return redirect("/")

    # Used to delete an item
    @app.route('/rem', methods=['POST'])
    def remove_item():
        card_id=str(request.form.get('item_id'))
        updateTrelloCard(card_id, {}, "DELETE", key, token)
        return redirect("/")

    #Funtions to work with Trello cards
    # Used to update an item
    def updateTrelloCard (cardId, newState, method, key, token):
        url='https://api.trello.com/1/cards/'+cardId+'?key='+key+'&token='+token
        res=requestJson(method,url, newState)
        return res

        
    # Used to get the item cards from a given Trello board
    def getTrelloCards(boardId, key, token):
        cards=[]      
        trelloLists=getTrelloLists(boardId, key, token)    
        cardDict=getTrelloItems(boardId, 'cards', key, token)
            
        for card in cardDict:
            cards.append(ToDoItem(trelloLists, card))
        return cards

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
    return app