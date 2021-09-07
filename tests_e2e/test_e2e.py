import os
from threading import Thread
import pytest
from selenium import webdriver
import requests
from todo_app.app import create_app

def requestJson (method, url, args):
    r = requests.request(method, url, params=args) 
    r.raise_for_status()
    print(r.raise_for_status())
    return r.json()
    
    
#Function to create trello board
def createTrelloBoard(boardName):
    url='https://api.trello.com/1/boards/'
    params={
            'key': os.getenv('TRELLO_KEY'),
            'token': os.getenv('TRELLO_TOKEN'),
            'name': boardName
        }
    
    res=requestJson("POST",url, params)
    return res


#Function to remove trello board
def deleteTrelloBoard(boardId):
    url='https://api.trello.com/1/boards/'+boardId
    res=requestJson("DELETE",url, {})
    return res

@pytest.fixture(scope='module')
def app_with_temp_board():
    # Create the new board & update the board id environment variable
    board_id = (createTrelloBoard('Selenium_Test_Board'))["id"]
    os.environ['trelloBoardID'] = board_id
    
    # construct the new application
    app = create_app()
    
    # start the app in its own thread.
    thread = Thread(target=lambda:app.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    
    yield app
    
    # Tear Down
    thread.join(1)
    #deleteTrelloBoard(board_id)


@pytest.fixture(scope='module')
def driver():
    with webdriver.Firefox() as driver:
        yield driver


def test_mainPage(driver):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'          

