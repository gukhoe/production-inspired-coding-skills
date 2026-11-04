import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def send(url, event):
    request = Request(url, data=json.dumps(event).encode(), headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urlopen(request, timeout=2) as response:
            return response.status, json.load(response)
    except HTTPError as error:
        with error:
            return error.code, json.load(error)
