# coding: utf-8

import json


class Json:
    def __init__(self, file_path):
        self.file_path = file_path

    def to_json(obj):
        return json.dumps(obj, default=lambda o: o.__dict__, indent=4)



