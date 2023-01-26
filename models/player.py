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
        self.score = float(0)
        self.has_played = []

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def sign_in_player(self, tournament):
        """
        Calls tournament sign-in player method. It allows to double-way sign-in player, either
        from the tournament object or from the player object.
        """
        tournament.sign_in_player(self)

    def set_score(self, score: float):
        """
        Updates player score after a match
        :param score: score number to be added to the player total score
        :type score: float
        :return: None
        :rtype: None
        """
        self.score += score

    def set_has_played(self, player):
        """
        Updates the list of played players after a match
        :param player: last match's opponent to be added to the list
        :type player: Player
        :return: None
        :rtype: None
        """
        if len(self.has_played) == 0:
            self.has_played.append(player.national_chess_identifier)
        else:
            for played_player in self.has_played:
                if played_player == player.national_chess_identifier:
                    pass
            else:
                self.has_played.append(player.national_chess_identifier)

