# coding: utf-8

import random

from models.tournament import Tournament
from models.json_file import ProgramData
from models.round import Round


class ControlRound:

    def is_current_round_initialised(self, program_file: ProgramData):
        current_round = program_file.get_current_round()
        if not current_round.match_list:
            return False
        else:
            return True

    def initialise_round(self, program_file: ProgramData):
        """
        Initializes round1 in a given tournament by :
        - Listing pairs of participants that will confront each other
        - Updating the round with the list of pairs
        - Increasing the current round number
        :param program_file: program file with the tournament where to initialise round 1
        :type program_file: ProgramData
        :return: None
        :rtype: None
        """
        current_tournament = program_file.get_last_tournament()
        current_round = current_tournament.current_round
        if current_round == 1:
            # Create randon pair list
            pair_list = self.set_pair_list_random(current_tournament)
        else:
            pair_list = self.set_pair_list_based_on_scores()

        # Update the match list to the current_round of the tournament
        current_tournament.set_round_match_list(current_round, pair_list)

    def set_pair_list_random(self, tournament: Tournament) -> list:
        """
        Shuffles participant list and creates random pairs returned as a list of pairs to play each other
        :param tournament: a given tournament for which we want to create random pairs
        :type tournament: tournament class
        :return: list of pairs
        :rtype: list
        """
        player_list = tournament.get_player_list()
        # Shuffle player list
        random.shuffle(player_list)
        pair_list = []
        # Get number of player per round
        number_of_matches_per_round = tournament.get_number_of_matches_per_round()
        # For each match, create a pair of players to play each other and add to list
        for match_number in range(0, len(player_list), number_of_matches_per_round):
            # Each pair is a list formed by [player, score]
            pair = [[player_list[match_number], 0], [player_list[match_number + number_of_matches_per_round - 1], 0]]
            # The pair (list type) is appended to the global pair list.
            pair_list.append(pair)
        return pair_list

    def set_pair_list_based_on_scores(self, tournament: Tournament) -> list:
        pair_list = []
        # TODO: code code code
        return pair_list
