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
        """

        :param player1:
        :type player1:
        :param player2:
        :type player2:
        :return:
        :rtype:
        """
        self.match_data = tuple((player1, player2))

    def get_player_national_chess_identifier(self, player_number: int) -> str:
        """
        Gets national chess identifier of one of the match players
        :param player_number: player number : 1 or 2
        :type player_number: int
        :return: national chess identifier of the selected player
        :rtype: str
        """
        player_data = self.match_data[player_number]
        player_national_chess_identifier = player_data[0]
        return player_national_chess_identifier

    def get_player_score(self, player_number: int) -> float:
        """
        Returns the score from one of the players of a match
        :param player_number: number of the player we want to get the score
        :type player_number: int
        :return: player score for the selected player
        :rtype: int
        """
        player_data = self.match_data[player_number]
        player_score = player_data[1]
        return player_score
