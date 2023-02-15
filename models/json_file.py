# coding: utf-8

import json

from models.tournament import Tournament
from models.round import Round
from models.match import Match
from models.player import Player
from models.player_in_tournament import PlayerInTournament


class ProgramData:
    """
    Tournament manger JSON data management.
    """
    def __init__(self, program_file_path):
        # JSON file path. To be executed from project root
        self.file_path = program_file_path
        self.ongoing_tournament = False
        self.player_dict = {}
        self.tournament_list = []

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def update_json_file(self):
        """
        Updates json program file
        :return: None
        :rtype:
        """
        try:
            with open(self.file_path, "r+") as file:
                json.dump(self, file, indent=4, cls=MyEncoder)
        except json.JSONDecodeError:
            print("problème avec le fichier player.json")
        except FileNotFoundError:
            print(f'fichier {self.file_path} inexistant')

    def add_new_tournament(self, tournament: Tournament):
        """
        Adds new tournament in position 0 of the tournament list
        :param tournament: tournament to be added
        :type tournament: Tournament
        :return: None
        :rtype:
        """
        self.tournament_list.insert(0, tournament)
        self.ongoing_tournament = True
        self.update_json_file()

    def add_player(self, player: Player):
        """
        Signs-in the tournament a given player
        :param player: player to be signed-in the tournament
        :type player: Player
        :return: None
        :rtype:
        """
        self.player_dict[player.national_chess_identifier] = player
        self.update_json_file()

    def update_data_object_from_json(self):
        """
        Updates tournament object with json file data and returns it
        as an object
        :return: None
        :rtype:
        """
        try:
            with open(self.file_path, "r") as file:
                file_data = json.load(file)
                self.file_path = file_data['file_path']
                self.ongoing_tournament = file_data['ongoing_tournament']
                file_tournament_list = file_data['tournament_list']
                player_dict = file_data['player_dict']
                for tournament_data in file_tournament_list:
                    tournament = Tournament(
                        name=tournament_data['name'],
                        place=tournament_data['place'],
                        start_date=tournament_data['start_date'],
                        end_date=tournament_data['end_date'],
                        description=tournament_data['description'],
                        rounds=tournament_data['total_rounds'],
                        current_round=tournament_data['current_round'],
                        status=tournament_data['status']
                    )
                    for json_round in tournament_data['round_list']:
                        # Initialise round object for each item of the
                        # round list
                        tournament_round = Round(
                            round_number=json_round['round_number'],
                            start_datetime=json_round['start_datetime'],
                            end_datetime=json_round['end_datetime'],
                            next_match=json_round['next_match']
                        )
                        # For each match in the json file create object
                        # Match and append to match list
                        for json_match in json_round['match_list']:
                            match_data = json_match['match_data']
                            match = Match(match_data[0], match_data[1])
                            # Append match to the tournament round
                            tournament_round.match_list.append(match)
                        # Insert round in the round list round's
                        # position (round_number -1)
                        tournament.round_list[int(json_round['round_number'])
                                              - 1] = tournament_round
                    # save players list
                    tournament.player_list = tournament_data['player_list']
                    for value in tournament_data['player_dict'].values():
                        player_in_tournament = PlayerInTournament(
                            national_chess_identifier=value[
                                'national_chess_identifier'],
                            score=value['score'],
                            has_played=value['has_played']
                        )
                        tournament.player_dict[
                            player_in_tournament.national_chess_identifier] \
                            = player_in_tournament
                    # append tournament to tournament program file
                    self.tournament_list.append(tournament)

                # parse player_dict values in order to create player objects
                # and add them to the program file
                for value in player_dict.values():
                    player = Player(
                        value['first_name'],
                        value['last_name'],
                        value['birth_date'],
                        value['national_chess_identifier'])
                    # create dict entry with player object
                    self.player_dict[player.national_chess_identifier] = player

        except json.JSONDecodeError as error:
            # In case of empty file, we return the empty player list
            print(error)
        except FileNotFoundError:
            print(f'fichier {self.file_path} inexistant')

    def get_player(self, national_chess_identifier: str) -> Player:
        """
        Call to get a player with a given national_chess_identifier
        :param national_chess_identifier: national chess identifier of
        the player we want to obtain
        :type national_chess_identifier: str
        :return: player corresponding to the national chess identifier
        given as a parameter
        :rtype: Player
        """
        player = self.player_dict[national_chess_identifier]
        return player

    def update_ongoing_tournament(self, tournament: Tournament):
        """

        :param tournament:
        :type tournament:
        :return: None
        :rtype:
        """
        self.tournament_list[0] = tournament
        self.update_json_file()

    def get_last_tournament(self) -> Tournament:
        """
        Returns last tournament added to the tournament list
        (last tournament added in time)
        :return: last tournament added to the program
        :rtype: Tournament
        """
        tournament_list = self.tournament_list
        last_tournament = tournament_list[0]
        return last_tournament

    def start_tournament(self):
        """
        Launches tournament after the signing-in phase
        :return: None
        :rtype:
        """
        tournament = self.get_last_tournament()
        # set tournament status to "running"
        tournament.set_status_running()
        # Set current round number to 1
        tournament.increase_round_number()
        self.update_json_file()

    def get_current_round(self) -> Round:
        """
        Returns ongoing round
        :return: ongoing round
        :rtype: Round
        """
        try:
            last_tournament = self.get_last_tournament()
            current_round_number = last_tournament.current_round
            current_round = last_tournament.round_list[current_round_number-1]
            return current_round
        except IndexError:
            pass

    def set_tournament_round_match_list(self, match_list: list):
        """
        Updates the match list of a round
        :param match_list: list of matches to be set in a round
        :type match_list: list
        :return: nothing
        :rtype:
        """
        # get ongoing tournament
        tournament = self.get_last_tournament()
        # set ongoing tournament match list
        tournament.set_round_match_list(match_list)
        # update ongoing tournament
        self.update_ongoing_tournament(tournament)

    def increase_round_number(self):
        """
        Increases the round number of the ongoing tournament
        :return: nothing
        :rtype:
        """
        ongoing_tournament = self.get_last_tournament()
        ongoing_tournament.increase_round_number()
        self.update_json_file()

    def get_player_dict(self) -> dict:
        """
        Returns the player dict of the program
        :return: player dict with all players saved in the program
        :rtype: dict
        """
        return self.player_dict

    def get_tournament_list(self) -> list:
        """
        Returns the list of tournaments saved in the program file
        :return: tournament list
        :rtype: list
        """
        return self.tournament_list

    def get_tournament(self, tournament_position: int) -> Tournament:
        """
        Retourns a tournament in a given position of the tournament list
        :param tournament_position: position in the list for which we want
        to get the tournament
        :type tournament_position: int
        :return: tournament objet saved in the position given as a parameter
        :rtype: Tournament
        """
        tournament_list = self.get_tournament_list()
        return tournament_list[tournament_position]


class MyEncoder(json.JSONEncoder):
    """"
    Returns dictionary with data in JSON format
    """
    def default(self, o):
        return o.__dict__
# ça ne sert pas vraiment ?
