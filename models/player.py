# coding: utf-8

import json


class Player:
    """
    Class for object Player
    """
    def __init__(self, first_name, last_name, birth_date, national_chess_identifier):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.national_chess_identifier = national_chess_identifier
        self.score = 0
        self.has_played = []

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def sign_in_player(self, tournament):
        """
        Calls tournament sign-in player method. It allows to double-way sign-in player, either
        from the tournament object or from the player object.
        """
        tournament.sign_in_player(self)


