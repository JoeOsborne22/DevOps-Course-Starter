import pytest
from dotenv import find_dotenv,load_dotenv
from todo_app.app import create_app
from unittest.mock import patch, Mock
import mongomock,os,pymongo


@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)


    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
    
        test_app = create_app()    

        with test_app.test_client() as client:
            yield client


#@patch('requests.request')
def test_index_page(client):
    #mock_get_requests.side_effect = mockResponse('test')

    addMockData()
    

    response = client.get('/')
    responseCode = response.status_code
    responseHtml = response.data.decode()
    assert responseCode == 200
    #assert "testDoingTask" in responseHtml
    #assert "testDoneTask" in responseHtml
    #assert "testDoingTask_UID:1548993486125" in responseHtml


def addMockData():

    mongoDB=os.getenv('MONGO_DB_NAME')
    mongoTable=os.getenv('MONGO_COLLECTION_NAME')
    mongoConnection=os.getenv('MONGO_CONNECT')
    client=pymongo.MongoClient(str(mongoConnection))
    db = client[mongoDB]
    table = db[str(mongoTable)]

    table.insert_many(responseCardsStub)

    return 


responseCardsStub = [
            {
                "name": "testDoTask_UID:1548993486146",
                "status": "To Do",
                "due": None,
                "dateLastActivity": "2021-08-20T00:00:00.000Z"
            },
            {
                "name": "testDoingTask_UID:1548993486125",
                "status": "Doing",
                "due": None,
                "dateLastActivity": "2021-08-20T00:00:00.000Z"
            },
            {
                "name": "testDoneTask_UID:1548993486114",
                "status": "Done",
                "due": None,
                "dateLastActivity": "2021-08-20T00:00:00.000Z"
            }
    
]



