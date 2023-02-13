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
        :rtype: None
        """
        try:
            with open(self.file_path, "r+") as file:
                json.dump(self, file, indent=4, cls=MyEncoder)
        except json.JSONDecodeError:
            print("problème avec le fichier player.json")
        except FileNotFoundError:
            print(f'fichier {self.file_path} inexistant')

    def erase_file_data(self):
        """
        Erases tournament json file data
        :return: None
        :rtype: None
        """
        with open(self.file_path, 'w'):
            pass

    def add_new_tournament(self, tournament: Tournament):
        self.tournament_list.insert(0, tournament)
        self.ongoing_tournament = True
        self.update_json_file()

    def add_player(self, player: Player):
        """
        Signs-in the tournament a given player
        :param player: player to be signed-in the tournament
        :type player: player
        :return: None
        :rtype: None
        """
        self.player_dict[player.national_chess_identifier] = player
        self.update_json_file()

    def update_data_object_from_json(self):
        """
        Updates tournament object with json file data and returns it as an object
        :return: None
        :rtype: None
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
                        # Initialise round object for each item of the round list
                        tournament_round = Round(
                            round_number=json_round['round_number'],
                            start_datetime=json_round['start_datetime'],
                            end_datetime=json_round['end_datetime'],
                            next_match=json_round['next_match']
                        )
                        # For each match in the json file create object Match and append to match list
                        for json_match in json_round['match_list']:
                            match_data = json_match['match_data']
                            match = Match(match_data[0], match_data[1])
                            # Append match to the tournament round
                            tournament_round.match_list.append(match)
                        # Insert round in the round list round's position (round_number -1)
                        tournament.round_list[int(json_round['round_number']) - 1] = tournament_round
                    # save players list
                    tournament.player_list = tournament_data['player_list']
                    for value in tournament_data['player_dict'].values():
                        player_in_tournament = PlayerInTournament(
                            national_chess_identifier=value['national_chess_identifier'],
                            score=value['score'],
                            has_played=value['has_played']
                        )
                        tournament.player_dict[player_in_tournament.national_chess_identifier] = player_in_tournament
                    # append tournament to tournament program file
                    self.tournament_list.append(tournament)

                # parse player_dict values in order to create player objects and add them to the program file
                for value in player_dict.values():
                    player = Player(value['first_name'], value['last_name'], value['birth_date'],
                                    value['national_chess_identifier'])
                    # create dict entry with player object
                    self.player_dict[player.national_chess_identifier] = player

        except json.JSONDecodeError as error:
            # In case of empty file, we return the empty player list
            print(error)
        except FileNotFoundError:
            print(f'fichier {self.file_path} inexistant')

    def get_player(self, national_chess_identifier: str) -> Player:
        player = self.player_dict[national_chess_identifier]
        return player

    def update_ongoing_tournament(self, tournament: Tournament):
        self.tournament_list[0] = tournament
        self.update_json_file()

    def get_last_tournament(self) -> Tournament:
        tournament_list = self.tournament_list
        last_tournament = tournament_list[0]
        return last_tournament

    def set_score(self, round_number: int, match_number: int, score_player1: list, score_player2: list):
        # Updating tournament matchs
        current_tournament = self.get_last_tournament()
        current_tournament.set_score(round_number, match_number, score_player1, score_player2)

        # updating player's score
        national_chess_id_player1 = score_player1[0]
        national_chess_id_player2 = score_player2[0]
        score1 = score_player1[1]
        score2 = score_player2[1]
        player1 = self.get_player(national_chess_id_player1)
        player2 = self.get_player(national_chess_id_player2)
        player1.set_score(score1)
        player2.set_score(score2)

        # updating player's opponent "has_played" list
        player1.set_has_played(player2)
        player2.set_has_played(player1)

    def start_tournament(self):
        tournament = self.get_last_tournament()
        # set tournament status to "running"
        tournament.set_status_running()
        # Set current round number to 1
        tournament.increase_round_number()
        self.update_json_file()

    def get_current_round(self) -> Round:
        try:
            last_tournament = self.get_last_tournament()
            current_round_number = last_tournament.current_round
            current_round = last_tournament.round_list[current_round_number-1]
            return current_round
        except IndexError as error:
            return None

    def set_tournament_round_match_list(self, match_list: list):
        # get ongoing tournament
        tournament = self.get_last_tournament()
        # set ongoing tournament match list
        tournament.set_round_match_list(match_list)
        # update ongoing tournament
        self.update_ongoing_tournament(tournament)

    def increase_round_number(self):
        ongoing_tournament = self.get_last_tournament()
        ongoing_tournament.increase_round_number()
        self.update_json_file()

    def get_player_dict(self):
        return self.player_dict

    def get_tournament_list(self):
        return self.tournament_list

    def get_tournament(self, tournament_position):
        tournament_list = self.get_tournament_list()
        return tournament_list[tournament_position]


class MyEncoder(json.JSONEncoder):
    """"
    Returns dictionary with data in JSON format
    """
    def default(self, o):
        return o.__dict__
# ça ne sert pas vraiment ?
