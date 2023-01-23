# coding: utf-8

import os
import json
from json import JSONEncoder


class PlayerList:
    def __init__(self):
        self.file_path = os.path.abspath("../data/players.json")
        self.player_list = []
        self.file_data = {"player_list": self.player_list}

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def update_json(self, player):
        """
        Updates json player file

        Parameters
        -------
        self
        player

        Returns
        -------
        None
        """

        try:
            self.player_list = self.get_player_list_from_json()
            self.append_player_to_list(player)
            self.file_data['player_list'] = self.player_list

            with open(self.file_path, "r+") as file:
                json.dump(self.file_data, file, indent=4, cls=MyEncoder)
        except json.JSONDecodeError:
            print("problème avec le fichier player.json")
        except FileNotFoundError:
            print(f'fichier {self.file_path} inexistant')

    def get_player_list_from_json(self):
        """
        Saves player list from json file to local memory
        """
        try:
            with open(self.file_path, "r") as file:
                self.file_data = json.load(file)
            self.player_list = self.file_data['player_list']
            return self.player_list
        except json.JSONDecodeError:
            # In cas of empty file, we return the empty player list
            print('fichier vide')
            return self.player_list
        except FileNotFoundError:
            print(f'fichier {self.file_path} inexistant')
            return self.player_list

    def append_player_to_list(self, player):
        """"
        Appends player to in-memory player_list
        """
        self.player_list = self.get_player_list_from_json()
        self.player_list.append(player)
        return self.player_list


class MyEncoder(JSONEncoder):
    """"
    Returns dictionary with data in JSON format
    """
    def default(self, o):
        return o.__dict__
# ça ne sert pas vraiment ?