from flask import Flask
from flask import render_template
from todo_app.data import session_items
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    #si.get_items()
    items=session_items.get_items()
    print (items)
    return render_template('index.html',list=items)


if __name__ == '__main__':
    app.run()
