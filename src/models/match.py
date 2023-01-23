# coding: utf-8

import json


class Match:
    def __init__(self, player1, player2):
        score_player1 = [player1]
        score_player2 = [player2]
        self.match_data = (score_player1, score_player2)
        # Commenter
        pass

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def set_score(self, score_player1, score_player2):
        self.match_data = (score_player1, score_player2)

