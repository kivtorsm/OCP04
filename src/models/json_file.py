# coding: utf-8

import json
from json import JSONEncoder


class Json:
    def __init__(self, file_path):
        self.file_path = file_path

    def to_json(obj):
        return json.dumps(obj, default=lambda o: o.__dict__, indent=4)


class MyEncoder(JSONEncoder):
    """"
    Returns dictionary with data in JSON format
    """
    def default(self, o):
        return o.__dict__
# ça ne sert pas vraiment ?
