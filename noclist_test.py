import pytest
from unittest.mock import patch, Mock
import noclist  

# Test for retry_request with a successful first try
def test_retry_request_success(monkeypatch):
    mock_response = Mock()
    mock_response.status_code = 200
    monkeypatch.setattr("requests.request", Mock(return_value=mock_response))
    
    response = noclist.retry_request('GET', 'http://fakehost/auth')
    assert response.status_code == 200

# Test for get_auth_token successfully retrieving a token
def test_get_auth_token_success(monkeypatch):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.headers = {'Badsec-Authentication-Token': '12345'}
    monkeypatch.setattr("noclist.retry_request", Mock(return_value=mock_response))

    token = noclist.get_auth_token('http://fakehost')
    assert token == '12345'

# Test for get_user_list successfully retrieving a list
def test_get_user_list_success(monkeypatch):
    mock_response = Mock()
    mock_response.text = '"18207056982152612516"\n"7692335473348482352"'
    mock_response.status_code = 200
    monkeypatch.setattr("noclist.retry_request", Mock(return_value=mock_response))
    
    user_list = noclist.get_user_list('http://fakehost', '12345')
    # Ensure it returns a JSON string
    assert '18207056982152612516' in user_list
    assert '7692335473348482352' in user_list

# Test handling failure to retrieve the auth token
def test_get_auth_token_failure(monkeypatch):
    monkeypatch.setattr("noclist.retry_request", Mock(side_effect=noclist.requests.RequestException))
    
    token = noclist.get_auth_token('http://fakehost')
    assert token is None

# Test handling failure to retrieve the user list
def test_get_user_list_failure(monkeypatch):
    monkeypatch.setattr("noclist.retry_request", Mock(side_effect=noclist.requests.RequestException))
    
    user_list = noclist.get_user_list('http://fakehost', '12345')
    assert user_list is None

 
def test_main_ok(monkeypatch, capsys):

    monkeypatch.setattr("noclist.get_auth_token", Mock(return_value='12345'))
    monkeypatch.setattr("noclist.get_user_list", Mock(return_value='["9757263792576857988", "7789651288773276582"]'))

    mock_arg = Mock()
    mock_arg.host = 'http://fakehost'

    with pytest.raises(SystemExit) as e:
         noclist.main(mock_arg)
    assert e.type == SystemExit
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert captured.out == '["9757263792576857988", "7789651288773276582"]\n'


def test_main_fail(monkeypatch, capsys):

    monkeypatch.setattr("noclist.get_auth_token", Mock(return_value='12345'))
    monkeypatch.setattr("noclist.get_user_list", Mock(return_value=None))

    mock_arg = Mock()
    mock_arg.host = 'http://fakehost'

    with pytest.raises(SystemExit) as e:
         noclist.main(mock_arg)
    assert e.type == SystemExit
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == ''

