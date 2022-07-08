from operator import attrgetter
from todo_app.flask_config import Config
import flask_login
from todo_app.viewModel import taskCards
from flask import Flask, render_template, request, redirect, session
import os,requests,pymongo,pprint,datetime
from todo_app.ToDoItem  import  ToDoItem
from todo_app.user import User
from bson.objectid import ObjectId
from flask_login import LoginManager, current_user, login_required, user_unauthorized
import uuid
import oauthlib.oauth2 as auth
from functools import wraps



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    app.config['LOGIN_DISABLED']=os.getenv('LOGIN_DISABLED') == "True"

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

    #setup Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def unauthenticated():
        
        state = str(uuid.uuid4())
        session['state']=state
        url = f"https://github.com/login/oauth/authorize?client_id={os.getenv('OAUTH_CLIENT_ID')}&state={state}"

        return redirect(url)

    #Route when user not authenticated
    @app.route('/login/callback')
    def authenticate_user():
        if (not 'state' in session) or (session['state'] != request.args['state']):
                return render_template('unauthorised.html')
        if "error" in request.args:
            return render_template('unauthorised.html')
        code = request.args['code']
        url = "https://github.com/login/oauth/access_token"
        headers = {
            "Accept": "application/json"
        }
        params = {
            "client_id": os.getenv('OAUTH_CLIENT_ID'),
            "client_secret": os.getenv('OAUTH_CLIENT_SECRET'),
            "code": code
        }
        resp = requests.request("POST",url,headers=headers,params=params)
        if not resp.ok:
            return render_template('unauthorised.html')
      
        access_token = resp.json()["access_token"]
        headers['Authorization'] = "token " + access_token
        url = "https://api.github.com/user"
        user_response = requests.request("GET",url,headers=headers,params=params)
      
        if not user_response.ok:
            return render_template('unauthorised.html')
      
        user_id = user_response.json()["id"]
        user = User(user_id)
        logged_in = flask_login.login_user(user)
        
        return redirect("/")    
        

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)
        
    def write_check(func):
        @wraps(func)
        def wrapper_write_check(*args, **kwargs):
            
            allowed = os.getenv('LOGIN_DISABLED')=='True' or user.role == "edit"
            user = flask_login.current_user
            
            if allowed:
                return func(*args, **kwargs)
            else:
                return render_template('unauthorised.html'),401
        return wrapper_write_check

    #Main functions/app urls
    # Main Page - will query for cards and display
    @app.route('/')
    @login_required
    def index():
        cards=getCards()
        if "sortAttr" in session:
            attrKey=attrgetter(session.get('sortAttr'))
            cards=sorted(cards, key=attrgetter(session.get('sortAttr')))
        item_view_model= taskCards(cards)

        user = flask_login.current_user
        edit = os.getenv('LOGIN_DISABLED')=='True' or user.role == "edit"
        return render_template('index.html',viewModel=item_view_model, edit=edit)

    # Used to add new item
    @app.route('/add', methods=['POST'])
    @login_required
    @write_check
    def add_item():
        card_title=request.form.get('item_name')
        card_desc=request.form.get('item_desc')
        card_due=request.form.get('item_due')
        card_lastActivity=datetime.datetime.utcnow()
        if not card_title == "": 
            cardDetails={"idList":defaultStatus,"name":card_title,"pos":"top","desc":card_desc,"due":card_due,"dateLastActivity":card_lastActivity}
            updateCard(cardDetails, "POST") 
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
    @login_required
    @write_check
    def alter_item():
        newState=str(request.form.get('item_state'))
        itemId=request.form.get('item_id')

        updQuery={"_id":ObjectId(itemId)},{"$set":{"idList":newState}}
        updateCard(updQuery,"PUT")
        
        return redirect("/")

    # Used to delete an item
    @app.route('/rem', methods=['POST'])
    @login_required
    @write_check
    def remove_item():
        card_id=ObjectId(request.form.get('item_id'))
        updateCard({"_id":card_id},"DELETE")
        return redirect("/")

    #Funtions to work with cards       
    # Used to get the item cards from DB
    def getCards():
        cards=[]
        for todoCard in todoCards.find():
            cards.append(ToDoItem(todoCard))

        return cards


    # Used to update an item
    def updateCard (newState, method):
        try: res=actionMap[method](newState)
        except: res=actionMap[method](newState[0],newState[1])
        
        return res

    return app