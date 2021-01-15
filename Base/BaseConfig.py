import requests

from urllib3 import disable_warnings
from urllib3.connectionpool import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)

import json


def get(**kwargs):
    data = {}
    url = kwargs["protocol"] + "://" + kwargs["host"] + kwargs["url"]
    print(url)
    r = requests.get(url, headers=kwargs.get("headers", None), verify=False)
    if r.status_code == 200 and len(r.text) > 0:
        r.encoding = 'UTF-8'
        data = json.loads(r.text)
    data["status_code"] = r.status_code

    return data


def post(files=None, **kwargs):
    result = {}

    url = kwargs["protocol"] + "://" + kwargs["host"] + kwargs["url"]
    data = None
    if kwargs.get("data", "none") != "none":
        data = json.dumps(kwargs["data"])
        print(data)
    print(url)
    r = requests.post(url, files=files, data=data, verify=False, headers=kwargs["headers"])
    result["status_code"] = r.status_code
    if r.status_code == 200 and len(r.text) > 0:
        r.encoding = 'UTF-8'
        result = json.loads(r.text)
    result["status_code"] = r.status_code
    return result


def post_login(**kwargs):
    result = {}

    url = kwargs["protocol"] + "://" + kwargs["host"] + kwargs["url"]
    data = None
    if kwargs.get("data", "none") != "none":
        data = json.dumps(kwargs["data"])
        print(data)
    print(url)
    r = requests.post(url, data=data, verify=False, headers=kwargs["headers"])
    if len(r.text):
        r.encoding = 'UTF-8'
        result = json.loads(r.text)
    result["status_code"] = r.status_code
    if result["status_code"] == 200:
        result["cookie"] = r.headers.get("Set-Cookie")

    return result


if __name__ == '__main__':
    headers = {'content-type': 'application/json'}
    post(protocol="http", host="ivt3.hschefu.com", port=9199, url="/login",
         data={'password': '12345678', 'username': 'xiangjin'}, headers=headers)
