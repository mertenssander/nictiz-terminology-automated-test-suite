import os
from urllib.request import urlopen, Request
from urllib import parse
import json

def test_retrieve_token():
    payload = {
        'username' : os.getenv('termspace_bot_user'),
        'password' : os.getenv('termspace_bot_pass'),
        }
    data = parse.urlencode(payload).encode('ascii')
    req = Request('https://nl-prod-main.termspace.com/api/users/login', data)
    with urlopen(req) as response:
        result = json.loads(response.read())

    termspace_token = result.get('token',False)
    assert termspace_token != False
    return termspace_token

def test_two():
    print(test_retrieve_token())
