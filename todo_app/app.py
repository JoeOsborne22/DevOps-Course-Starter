from operator import itemgetter
from flask import Flask
from flask import render_template
from flask import request
from werkzeug.utils import redirect
from todo_app.data import session_items
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    items=(sorted(session_items.get_items(), key=itemgetter('status'),reverse=True))
    return render_template('index.html',list=items)


@app.route('/add', methods=['POST', 'GET'])
def add_item():
    if request.method == 'POST':
        user_item=request.form.get('item_name')
        if not user_item == "":
            session_items.add_item(user_item)
    return redirect("/")

@app.route('/mark', methods=['POST', 'GET'])
def alter_item():
    if request.method == 'POST':
        try:
            user_id=int(request.form.get('item_id'))
        except:
            user_id=0
        if (user_id > 0):
            item=session_items.get_item(str(user_id))
            if not item == None:
                item['status']='Completed'
                session_items.save_item(item)
    return redirect("/")

@app.route('/rem', methods=['POST', 'GET'])
def remove_item():
    if request.method == 'POST':
        try:
            user_id=int(request.form.get('item_id'))
        except:
            user_id=0
        if (user_id > 0):
            item=session_items.get_item(user_id)
            session_items.remove_item(item)
        newItems=session_items.get_items()
        for item in newItems:
            item['id']=newItems.index(item)+1
            session_items.save_item(item)
    return redirect("/")


if __name__ == '__main__':
    app.run()
