# coding: utf-8

import json
import datetime

from match import Match


class Round:
    def __init__(self, round_number):
        self.name = f"Round {round_number}"
        self.round_number = round_number
        self.start_datetime = 0
        self.end_datetime = 0
        self.match_list = []

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    # def __getitem__(self, index):
    #     return self.item[index]
    #
    # def __setitem__(self, index, item):
    #     self.item[index] = item

    def to_json(self):
        """
        Returns round object as a json string
        """
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def set_start_time(self):
        """
        Sets round start date_time
        """
        self.start_datetime = datetime.datetime.now().isoformat()

    def set_end_time(self):
        """
        Sets round end date_time
        """
        self.end_datetime = datetime.datetime.now().isoformat()

    def download_round_data(self, tournament, round_number):
        """
        Updates the round data with the given round of a tournament data
        :param tournament: tournament from which we get the data
        :type tournament: tournament
        :param round_number: round number data to be updated
        :type round_number: int
        :return: None
        :rtype: None
        """
        # Get round data from JSON file
        round_data = tournament.get_round_data(round_number)
        print(type(round_data))
        print(round_data)
        self.round_number = round_data['round_number']
        self.name = round_data['name']
        self.match_list = round_data['match_list']
        self.end_datetime = round_data['end_datetime']
        self.start_datetime = round_data['start_datetime']

    def initialize_match_list(self, tournament, match_list):
        """
        Initializes the match list in the round object
        """
        number_of_matches_per_round = tournament.get_number_of_matches_per_round()
        # For each match, we update de list of matches
        for match_number in range(number_of_matches_per_round):
            # A match list is formed of a list of pairs that will confront in a match
            pair = match_list[match_number]
            # Each pair is formed of a list of 2 players
            player1 = pair[0]
            player2 = pair[1]
            # A match object is declared
            match = Match(player1, player2)
            # The match is added to the round match list
            self.match_list.append(match)

    def get_match_list(self, tournament, round_number):
        """
        Returns the match list form the round
        :return: list of matches
        :rtype: list
        """
        self.download_round_data(tournament, round_number)
        return self.match_list