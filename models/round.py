# coding: utf-8

import json
import datetime

from models.match import Match


class Round:
    def __init__(self, round_number, start_datetime=0, end_datetime=0, match_list=[], next_match=1):
        self.name = f"Round {round_number}"
        self.round_number = round_number
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.match_list = match_list
        self.next_match = next_match

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def set_start_time(self):
        """
        Sets round start date_time
        :return: None
        :rtype: None
        """
        self.start_datetime = datetime.datetime.now().isoformat()

    def set_end_time(self):
        """
        Sets round end date_time
        :return: None
        :rtype: None
        """
        self.end_datetime = datetime.datetime.now().isoformat()

    def set_match_list(self, tournament, match_list):
        """
        Initializes the match list in the round object
        :param tournament: tournament in which the round is played
        :type tournament: Tournament
        :param match_list: list of matche sof the round to be set for the round
        :type match_list: list
        :return: None
        :rtype: None
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
    #     TODO : Comprendre pourquoi ça remplit tous les rounds du tournoi

    def get_match_list(self, tournament, round_number):
        """
        Returns the match list form the round
        :return: list of matches
        :rtype: list
        """
        return self.match_list

    def increment_next_match(self):
        """
        Increments the next_match attribute to indicate which match is to be played next
        :return: None
        :rtype: None
        """
        self.next_match += 1

    def set_current_match_score(self, match_score):
        self.match_list[self.next_match - 1] = match_score
