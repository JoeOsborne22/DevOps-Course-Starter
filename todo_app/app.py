from operator import attrgetter
from todo_app.viewModel import taskCards
from flask import Flask, render_template, request, redirect, session
import os,requests,pymongo,pprint,datetime
from todo_app.ToDoItem  import  ToDoItem
from bson.objectid import ObjectId
#from todo_app.createApp import createApp


def create_app():
    app = Flask(__name__)
    app.secret_key=os.getenv('TODO_APP_SECRET_KEY')

    # Set app variables
    #Setting up connection to MongoDB
    mongoConnection=os.getenv('MONGO_CONNECT')
    mongoDB=os.getenv('MONGO_DB_NAME')
    mongoTable=os.getenv('MONGO_TABLE_NAME')
    defaultStatus=os.getenv('MONGO_DEFAULT_STATUS')
    client=pymongo.MongoClient(str(mongoConnection))
    db = client[mongoDB]
    todoCards = db[str(mongoTable)]
    
    # Map used to determine which function to use when interacting with DB
    actionMap={
        'POST':todoCards.insert_one,
        'PUT':todoCards.update_one,
        'DELETE':todoCards.delete_one
    }

    #Main functions/app urls
    # Main Page - will query for cards and display
    @app.route('/')
    def index():
        cards=getTrelloCards()
        if "sortAttr" in session:
            attrKey=attrgetter(session.get('sortAttr'))
            cards=sorted(cards, key=attrgetter(session.get('sortAttr')))
        item_view_model= taskCards(cards)
        return render_template('index.html',viewModel=item_view_model)

    # Used to add new item
    @app.route('/add', methods=['POST'])
    def add_item():
        card_title=request.form.get('item_name')
        card_desc=request.form.get('item_desc')
        card_due=request.form.get('item_due')
        card_lastActivity=datetime.datetime.utcnow()
        if not card_title == "": 
            cardDetails={"idList":defaultStatus,"name":card_title,"pos":"top","desc":card_desc,"due":card_due,"dateLastActivity":card_lastActivity}
            updateTrelloCard(cardDetails, "POST") 
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
        itemId=request.form.get('item_id')

        updQuery={"_id":ObjectId(itemId)},{"$set":{"idList":newState}}
        updateTrelloCard(updQuery,"PUT")
        
        return redirect("/")

    # Used to delete an item
    @app.route('/rem', methods=['POST'])
    def remove_item():
        card_id=ObjectId(request.form.get('item_id'))
        updateTrelloCard({"_id":card_id},"DELETE")
        return redirect("/")

    #Funtions to work with cards       
    # Used to get the item cards from DB
    def getTrelloCards():
        cards=[]
        for todoCard in todoCards.find():
            cards.append(ToDoItem(todoCard))

        return cards


    # Used to update an item
    def updateTrelloCard (newState, method):
        try: res=actionMap[method](newState)
        except: res=actionMap[method](newState[0],newState[1])
        
        return res

    return app