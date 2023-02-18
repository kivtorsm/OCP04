# coding: utf-8

import json

from models.round import Round
from models.player_in_tournament import PlayerInTournament


class Tournament:
    """"
    Player list contained in JSON file
    """

    def __init__(
            self,
            name,
            place,
            start_date,
            end_date,
            description,
            player_list=None,
            player_dict=None,
            rounds=4,
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
        self.player_list = player_list if player_list else []
        self.player_dict = player_dict if player_dict else {}

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def increase_round_number(self):
        """
        Increases the current round count
        :return: None
        :rtype:
        """
        self.current_round += 1

    def sign_in_player(self, national_chess_identifier: str):
        """
        Signs-in the tournament a given player
        :param national_chess_identifier: national chess identifier of the
        player to be signed-in
        :type national_chess_identifier: str
        :return: None
        :rtype:
        """
        self.player_list.append(national_chess_identifier)
        player_in_tournament = PlayerInTournament(national_chess_identifier)
        self.player_dict[player_in_tournament.national_chess_identifier] \
            = player_in_tournament

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
        return self.round_list

    def set_round_match_list(self, match_list):
        """
        Updates the list of matches of a given round with a new given
        list of matches
        :param match_list: the updated list of matches to set in the
        round match list
        :type match_list: list
        :return: No return
        :rtype: None
        """
        # create round object
        current_round = self.current_round
        tournament_round = self.round_list[current_round-1]
        # update round match list
        tournament_round.match_list = match_list
        # update tournament with round object
        self.round_list[current_round - 1] = tournament_round

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
        :param round_number: the round number for which we want the list
        of matches
        :type round_number: int
        :return: list of matches for a specified round
        :rtype: list
        """
        tournament_round = self.round_list[round_number - 1]
        return tournament_round.match_list

    def set_status_running(self):
        """
        Sets tournament status to running
        :return: nothing
        :rtype:
        """
        self.status = "running"

    def set_round_start_time(self):
        """
        Sets round start time to the current time
        :return: nothing
        :rtype:
        """
        current_round = self.get_round(self.current_round)
        current_round.set_start_time()
        self.round_list[self.current_round - 1] = current_round

    def set_round_end_time(self):
        """
        Sets round end time to the current time
        :return: nothing
        :rtype:
        """
        current_round_number = self.current_round
        current_round = self.get_round(current_round_number)
        current_round.set_end_time()
        self.round_list[self.current_round - 1] = current_round

    def get_player_in_tournament(self, national_chess_identifier: str) \
            -> PlayerInTournament:
        """
        Returns tournament player data
        :param national_chess_identifier: national chess ID of the player
        :type national_chess_identifier: str
        :return: player data in tournament
        :rtype: PlayerInTournament
        """
        player_in_tournament = self.player_dict[national_chess_identifier]
        return player_in_tournament

    def get_status_in_french(self) -> dict:
        """
        Translates tournament status into French
        :return: tournament status translated in French
        :rtype: str
        """
        status_dict = {
            "signing-in players": "Inscriptions joueurs",
            "running": "En cours",
            "finished": "Fini"
        }
        return status_dict[self.status]

    def get_player_dict(self) -> dict:
        """
        Returns player dict from the tournament
        :return: player dict of the tournament
        :rtype: dict
        """
        return self.player_dict
