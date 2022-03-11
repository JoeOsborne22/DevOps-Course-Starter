import pytest
from dotenv import find_dotenv,load_dotenv
from todo_app.app import create_app
from unittest.mock import patch, Mock
import mongomock


@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = create_app()
        
        with test_app.test_client() as client:
            yield client


@patch('requests.request')
def test_index_page(mock_get_requests, client):
    mock_get_requests.side_effect = mockResponse('test')

    response = client.get('/')
    responseCode = response.status_code
    responseHtml = response.data.decode()
    assert responseCode == 200
    assert "testDoingTask" in responseHtml
    assert "testDoneTask" in responseHtml
    assert "testDoingTask_UID:1548993486125" in responseHtml





def mockResponse(url):

        status=200,
        content="CONTENT",
        
        raise_for_status=None

        mock_resp = Mock()

        # set status code and content
        mock_resp.status_code = status
        mock_resp.content = content
        print(url)
        # add json data if provided
        
     
     
        mock_resp.json = Mock(return_value=responseCardsStub)
        return mock_resp


todoListId=0
doingListId=1
doneListId=2

todoItemId=98765
doingItemId=1248457
doneItemId=26563728


responseListsStub = [{
        "_id": todoListId,
        "name": "todo"   
    },
    {
        "_id": doingListId,
        "name": "Doing",
    },
    {
        "_id": doneListId,
        "name": "Done"
    }]


responseCardsStub = [
            {
                "_id": todoItemId,
                "name": "testDoTask",
                "idList": todoListId,
                "due": None,
                "dateLastActivity": "2021-08-20T00:00:00.000Z"
            },
            {
                "_id": doingItemId,
                "name": "testDoingTask_UID:1548993486125",
                "idList": doingListId,
                "due": None,
                "dateLastActivity": "2021-08-20T00:00:00.000Z"
            },
            {
                "_id": doneItemId,
                "name": "testDoneTask",
                "idList": doneListId,
                "due": None,
                "dateLastActivity": "2021-08-20T00:00:00.000Z"
            }
    
]



sample_trello_card = {
    "id": todoItemId,
    "name": "testNextTask"
}
