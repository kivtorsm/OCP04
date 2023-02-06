# coding: utf-8

import random

from models.tournament import Tournament
from models.json_file import ProgramData
from models.round import Round


class ControlRound:
    def __init__(self, round_view):
        # view
        self.round_view = round_view

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
        :param program_file: program file with the tournament where to initialize round 1
        :type program_file: ProgramData
        :return: No return
        :rtype: None
        """
        current_tournament = program_file.get_last_tournament()
        current_round_number = current_tournament.current_round
        if current_round_number == 1:
            # Create random pair list
            pair_list = ControlRound.set_pair_list_random(current_tournament)

        else:
            pair_list = self.set_pair_list_based_on_scores(current_tournament)

        # Update the match list to the current_round of the tournament
        program_file.set_tournament_round_match_list(pair_list)

    @staticmethod
    def set_pair_list_random(tournament: Tournament) -> list:
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
        for match_number in range(0, int(len(player_list)/2)):
            # Each pair is a list formed by [player, score]
            pair = [[player_list[match_number], 0], [player_list[match_number + number_of_matches_per_round], 0]]
            # The pair (list type) is appended to the global pair list.
            pair_list.append(pair)
        return pair_list

    def set_pair_list_based_on_scores(self, tournament: Tournament) -> list:
        pair_list = []
        # TODO: code code code
        return pair_list

    def set_match_score(self, program_file: ProgramData):
        current_round = program_file.get_current_round()
        current_match_number = current_round.next_match
        current_match = current_round.match_list[current_match_number - 1]
        match_score = self.round_view.prompt_for_score_input(current_match)
        current_round.match_list[current_round.next_match - 1]['match_data'] = match_score
        current_round.increment_next_match()
        current_tournament = program_file.get_last_tournament()

        # Verify if the round is finished in order to increase the next round number
        is_round_finished = self.is_round_finished(program_file)
        if is_round_finished:
            current_tournament.increase_round_number()

        # Update tournament data with the round data
        current_tournament.round_list[current_tournament.current_round - 1] = current_round
        # Update program_file with last tournament data and update json_file
        program_file.update_ongoing_tournament(current_tournament)


    @staticmethod
    def is_round_finished(program_file: ProgramData):
        current_round = program_file.get_current_round()
        return current_round.next_match > program_file.get_last_tournament().get_number_of_matches_per_round()

