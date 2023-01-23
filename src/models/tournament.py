# coding: utf-8

import os
import json

from json_file import MyEncoder


class Tournament:
    """"
    Player list contained in JSON file
    """
    def __init__(self, name, place, start_date, end_date, description, rounds=4):

        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = rounds
        self.current_round = 0
        self.description = description
        self.round_list = []
        for tournament_round in range(rounds):
            self.round_list.append(f"Round {str(tournament_round)}")
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
            return file_data
        except json.JSONDecodeError:
            # In case of empty file, we return the empty player list
            print('fichier vide')
            return None
        except FileNotFoundError:
            print(f'fichier {self.file_path} inexistant')
            return None

    def get_player_dict_from_json(self):
        """
        Saves player list from json file to local memory
        """
        file_data = self.get_data_from_json_file()
        self.player_dict = file_data['player_dict']

    def add_player_to_player_dict(self, player):
        self.get_player_dict_from_json()
        self.player_dict[player.national_chess_identifier] = player

    # def update_json(self):
    #     """
    #     Updates json player file
    #
    #     Parameters
    #     -------
    #     self
    #     player
    #
    #     Returns
    #     -------
    #     None
    #     """
    #
    #     try:
    #         self.append_player_to_list(player)
    #         self.file_data['player_list'] = self.player_list
    #
    #         with open(self.file_path, "r+") as file:
    #             json.dump(self.file_data, file, indent=4, cls=MyEncoder)
    #     except json.JSONDecodeError:
    #         print("problème avec le fichier player.json")
    #     except FileNotFoundError:
    #         print(f'fichier {self.file_path} inexistant')


