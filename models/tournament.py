# coding: utf-8

import json
import os

from models.round import Round


class Tournament:
    """"
    Player list contained in JSON file
    """

    def __init__(self, name, place, start_date, end_date, description, player_list=[], rounds=4,
                 status="signing-in players", current_round=0):

        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.total_rounds = rounds
        self.status = status
        self.current_round = current_round
        self.description = description
        self.round_list = []
        for round_number in range(self.total_rounds):
            tournament_round = Round(round_number + 1)
            self.round_list.append(tournament_round)
        self.player_list = player_list

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def increase_round_number(self):
        """
        Increases the current round count
        :return: None
        :rtype: None
        """
        self.current_round += 1

    def sign_in_player(self, national_chess_identifier: str):
        """
        Signs-in the tournament a given player
        :param national_chess_identifier: national chess identifier of the player to be signed-in
        :type national_chess_identifier: str
        :return: None
        :rtype: None
        """
        self.player_list.append(national_chess_identifier)

    def get_number_of_players(self):
        """
        Returns the number of players signed-in the tournament
        :return: Number of signed-in players
        :rtype: int
        """
        return len(self.player_list)

    def get_number_of_rounds(self):
        """
        Returns the number of rounds to be played in the tournament
        :return: number of rounds
        :rtype: int
        """
        return self.total_rounds

    def get_number_of_matches_per_round(self):
        """
        Returns the number of matches to be played in each round.
        It's equals to the number of players divided by 2.
        :return: number of players
        :rtype: int
        """
        return int(self.get_number_of_players() / 2)

    def get_player_list(self):
        """
        Returns the list of players signed-in the tournament
        :return: list of signed-in players
        :rtype: list
        """
        return self.player_list

    def get_round_list(self):
        """
        Returns the list of rounds to be played in the tournament
        :return: list of rounds to be played in the tournament
        :rtype: list
        """
        self.set_tournament_data_from_json_file()
        return self.round_list

    def set_round_match_list(self, round_number, match_list):
        """
        Updates the list of matches of a given round with a new given list of matches
        :param round_number: the round number where to update the list of matches
        :type round_number: int
        :param match_list: the updated list of matches to set in the round match list
        :type match_list: list
        :return: None
        :rtype: None
        """
        # create round object
        tournament_round = Round(round_number)
        # update round with json data
        tournament_round.set_match_list(self, match_list)
        # update tournament with round object
        self.round_list[round_number - 1] = tournament_round

    def get_round(self, round_number) -> Round:
        """
        Returns a given round data
        :param round_number: number of the round for which to get the data
        :type round_number: int
        :return: round data
        :rtype: Round
        """
        tournament_round = self.round_list[round_number - 1]
        return tournament_round

    def get_round_match_list(self, round_number) -> list:
        """
        Returns the match list from a specific round
        :param round_number: the round number for which we want the list of matches
        :type round_number: int
        :return: list of matches for a specified round
        :rtype: list
        """
        tournament_round = self.round_list[round_number - 1]
        return tournament_round.match_list

    def set_score(self, round_number: int, match_number: int, score_player1: list, score_player2: list):
        """
        Updates a given match score in a given round as well as concerned players' scores
        :param program_data: program current data
        :type program_data: ProgramData
        :param round_number: ongoing round number
        :type round_number: int
        :param match_number: played match number
        :type match_number: int
        :param score_player1: 2-elements list containing [player national_chess_ID: str, score: float]
        :type score_player1: list
        :param score_player2: 2-elements list containing [player nationa_chess_ID: str, score: float]
        :type score_player2: list
        :return: None
        :rtype: None
        """
        # saving Round object in variable
        tournament_round = self.round_list[round_number - 1]

        # saving match object invariable
        match = tournament_round.match_list[match_number - 1]

        # setting match players' score
        match.set_score(score_player1, score_player2)

        # updating the match in the round match list
        tournament_round.match_list[match_number - 1] = match

        # updating the round in the tournament round list
        self.round_list[round_number - 1] = tournament_round

    def set_status_running(self):
        self.status = "running"

