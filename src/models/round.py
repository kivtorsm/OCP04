# coding: utf-8

import json
import datetime


class Round:
    def __init__(self, name):
        self.name = name
        self.start_datetime = datetime.datetime.now()
        self.end_datetime = 0
        self.match_list = []
        self.match_couples = []

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def set_end_time(self):
        """
        Sets end date_time
        """
        self.end_datetime = datetime.datetime.now()

    def append_finished_match(self, match):
        self.match_list.append(match)

