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
    items=session_items.get_items()
    return render_template('index.html',list=items)

@app.route('/add', methods=['POST', 'GET'])
def add_item():
    if request.method == 'POST':
        user_item=request.form.get('item_name')
        if not user_item == "":
            session_items.add_item(user_item)
    return redirect("/")

if __name__ == '__main__':
    app.run()
