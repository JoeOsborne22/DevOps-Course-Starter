import pytest
from dotenv import find_dotenv,load_dotenv
from todo_app.createApp import createApp
from unittest.mock import patch, Mock
@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    test_app = createApp()
    with test_app.test_client() as client:
        yield client


@patch('requests.get')
def test_index_page(mock_get_requests, client):
    mock_get_requests.side_effect = mocklists

    response = client.get('/')
    responseCode = response.status_code
    assert responseCode == 200
    
responseStub = [1,3]

def mocklists(url, params):    
    if url == f'https://api.trello.com/1/boards/testTest/lists':
        response = Mock(ok=True)
        # responseStub used for mock data
        response.json.return_value =responseStub
        return response
    return None