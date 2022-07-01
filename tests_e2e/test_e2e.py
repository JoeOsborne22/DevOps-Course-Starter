import os
from threading import Thread
import pytest
from selenium import webdriver
import requests,pymongo
from todo_app.app import create_app
from dotenv import find_dotenv,load_dotenv
from selenium.webdriver.firefox.options import Options


def requestJson (method, url, args):
    r = requests.request(method, url, params=args) 
    r.raise_for_status()
    print(r.raise_for_status())
    return r.json()
    
    


#Function to remove selenium table
def deleteBoard():
    client=pymongo.MongoClient(str(os.getenv('MONGO_CONNECT')))
    db = client[os.getenv('MONGO_DB_NAME')]
    db[str(os.getenv('MONGO_TABLE_NAME'))].drop()
    return 

@pytest.fixture(scope='module')
def app_with_temp_board():
    # Load dotenv file before being used/referenced
    file_path = find_dotenv('.env')
    os.environ['LOGIN_DISABLED'] = 'True'
    load_dotenv(file_path, override=True)

    # Create & update the test DB environment variable, this will create a new board
    os.environ['MONGO_TABLE_NAME'] = 'Selenium_Test_Board'
    os.environ['LOGIN_DISABLED'] = 'True'
    
    # construct the new application
    app = create_app()
    
    # start the app in its own thread.
    thread = Thread(target=lambda:app.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    
    yield app
    
    # Tear Down
    thread.join(1)
    deleteBoard()


@pytest.fixture(scope='module')
def driver():
    opts = Options()
    opts.headless = True
    with webdriver.Firefox(options=opts) as driver:
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
    



