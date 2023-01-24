# coding: utf-8

import os
import json

from json_file import MyEncoder
from round import Round


class Tournament:
    """"
    Player list contained in JSON file
    """
    def __init__(self, name, place, start_date, end_date, description, rounds=4):

        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.total_rounds = rounds
        self.current_round = 0
        self.description = description
        self.round_list = []
        for round_number in range(self.total_rounds):
            tournament_round = Round(round_number + 1)
            self.round_list.append(tournament_round)
        self.player_dict = {}
        self.file_path = os.path.abspath(f"../../data/{self.name}.json")
        # TODO : adapt depending on execution

    def __str__(self):
        with open(self.file_path, "r") as file:
            data = json.load(file)
        return json.dumps(data, default=lambda o: o.__dict__, indent=4)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def erase_file_data(self):
        with open(self.file_path, 'w'):
            pass

    def write_json_file(self):
        """
        Updates json tournament file

        Parameters
        -------
        self

        Returns
        -------
        None
        """
        try:
            with open(self.file_path, "r+") as file:
                json.dump(self, file, indent=4, cls=MyEncoder)
        except json.JSONDecodeError:
            print("problème avec le fichier player.json")
        except FileNotFoundError:
            print(f'fichier {self.file_path} inexistant')

    def sign_in_player(self, player):
        self.add_player_to_player_dict(player)
        self.write_json_file()

    def get_data_from_json_file(self):
        try:
            with open(self.file_path, "r") as file:
                file_data = json.load(file)
                self.name = file_data['name']
                self.place = file_data['place']
                self.start_date = file_data['start_date']
                self.end_date = file_data['end_date']
                self.total_rounds = file_data['total_rounds']
                self.current_round = file_data['current_round']
                self.description = file_data['description']
                self.round_list = file_data['round_list']
                self.player_dict = file_data['player_dict']
            return file_data
        except json.JSONDecodeError:
            # In case of empty file, we return the empty player list
            print('fichier vide')
            return None
        except FileNotFoundError:
            print(f'fichier {self.file_path} inexistant')
            return None

    # def get_player_dict_from_json(self):
    #     """
    #     Saves player list from json file to local memory
    #     """
    #     file_data = self.get_data_from_json_file()
    #     self.player_dict = file_data['player_dict']

    def add_player_to_player_dict(self, player):
        # self.get_player_dict_from_json()
        self.player_dict[player.national_chess_identifier] = player

    def get_number_of_players(self):
        # self.get_player_dict_from_json()
        return len(self.player_dict)

    def get_number_of_rounds(self):
        return self.total_rounds

    def get_number_of_matches_per_round(self):
        return int(self.get_number_of_players()/2)

    def update_match_list(self, tournament_round, couples_list):
        # Get data from json
        self.get_data_from_json_file()
        # Update match list in the round object
        tournament_round.update_match_list(self.get_number_of_matches_per_round(), couples_list)
        # Update the tournament round list with the updated round object
        self.round_list[tournament_round.round_number - 1] = tournament_round
        # Save tournament to json file
        self.write_json_file()

    def get_player_list(self):
        # self.get_player_dict_from_json()
        player_list = list(self.player_dict.keys())
        return player_list

    def get_round_list(self):
        self.get_data_from_json_file()
        return self.round_list

    def update_round_match_list(self, round_number, match_list):
        self.get_data_from_json_file()
        # create round object
        tournament_round = Round(round_number)
        # update round with json data
        tournament_round.update_round_data(self, round_number)
        # update round with input match_list
        tournament_round.update_match_list(self, match_list)
        # update tournament with round object
        self.round_list[round_number-1] = tournament_round
        # update json file
        self.write_json_file()

    def get_round_data(self, round_number):
        round_data = self.round_list[round_number-1]
        return round_data


