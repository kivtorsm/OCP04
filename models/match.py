# coding: utf-8

import json


class Match:
    def __init__(self, player1, player2):
        self.match_data = tuple((player1, player2))

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def to_json(self):
        """
        Returns object as a json string
        :return: object as json string
        :rtype: str
        """
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def set_score(self, player1, player2):
        self.match_data = tuple((player1, player2))
