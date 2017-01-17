from nose.tools import *
from bin.app import app
from tests.tools import assert_response

def test_game_engine_index():
    # check that we get a 303 See Other on the / URL
    resp = app.request("/")
    assert_response(resp, status="303")
        
    # test our first GET request to /game and to / with status 303 because of See Other
    resp = app.request("/game")
    assert_response(resp)
    resp = app.request("/")
    assert_response(resp, status="303")
    
    # make sure default values work for the form
    resp = app.request("/game", method="POST")
    assert_response(resp, contains=None, status="303")
