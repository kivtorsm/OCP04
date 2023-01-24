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

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def set_start_time(self):
        """
        Sets end date_time
        """
        self.start_datetime = datetime.datetime.now().isoformat()

    def set_end_time(self):
        """
        Sets end date_time
        """
        self.end_datetime = datetime.datetime.now().isoformat()

    def update_match_list(self, tournament, match_list):
        number_of_matches_per_round = tournament.get_number_of_matches_per_round()
        for match_number in range(number_of_matches_per_round):
            couple = match_list[match_number]
            player1 = couple[0]
            player2 = couple[1]
            match = Match(player1, player2)
            self.match_list.append(match)

    def get_match_list(self):
        return self.match_list

    def update_round_data(self, tournament, round_number):
        round_data = tournament.get_round_data(round_number)
        self.round_number = round_data['round_number']
        self.name = round_data['name']
        self.match_list = round_data['match_list']
        self.end_datetime = round_data['end_datetime']
        self.start_datetime = round_data['start_datetime']


