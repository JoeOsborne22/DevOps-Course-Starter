import os
from threading import Thread
import pytest
from selenium import webdriver
import requests
from todo_app.app import create_app
from dotenv import find_dotenv,load_dotenv

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
def deleteTrelloBoard(boardId, key, token):
    url='https://api.trello.com/1/boards/'+boardId+'?key='+key+'&token='+token
    res=requestJson("DELETE",url, {})
    return res

@pytest.fixture(scope='module')
def app_with_temp_board():
    # Load dotenv file before being used/referenced
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

    # Create the new board & update the board id environment variable
    board = (createTrelloBoard('Selenium_Test_Board'))
    board_id = board["id"]

    key=os.getenv('TRELLO_KEY')
    token=os.getenv('TRELLO_TOKEN')
    os.environ['TRELLO_BOARD_ID'] = board_id
    
    #Hit up the trello board and find the id of the base list 
    url='https://api.trello.com/1/boards/'+board_id+'/'+'lists'+'?key='+key+'&token='+token
    res=requestJson("GET",url, {})
    os.environ['TRELLO_BASE_LIST']= res[0]["id"]

    # construct the new application
    app = create_app()
    
    # start the app in its own thread.
    thread = Thread(target=lambda:app.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    
    yield app
    
    # Tear Down
    thread.join(1)
    deleteTrelloBoard(board_id, key, token)


@pytest.fixture(scope='module')
def driver():
    with webdriver.Firefox() as driver:
        yield driver


def test_mainPage(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'  
    addNewTask(driver)  

    
    
def addNewTask(driver):
    name_input = driver.find_element_by_id('iname')
    name_input.send_keys('Test item')
    submit_button = driver.find_element_by_id('subBttn')
    submit_button.click()
    new_item_status = driver.find_element_by_id('todo')
    assert new_item_status is not None      
    



