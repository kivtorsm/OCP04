# coding: utf-8

import json
import os
from json import JSONEncoder


class Player:
    """
    Class for object Player
    """
    def __init__(self, first_name, last_name, birth_date, national_chess_identifier):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.national_chess_identifier = national_chess_identifier

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def add_player_to_list(self, player_list):
        player_list.update_json(self)
    # def date_has_right_format(self):
    #     """"
    #     Verifies that the birth date respects the defined date format
    #     """
    #     # TODO: implémenter test de format de date
    #     assert 1 == 1
    #     return True
    # def national_chess_identifier_has_right_format(self):
    #      """"
    #      Verifies that the national chess identifier has the right format
    #
    #      """
    #      # TODO: comprendre fonctionnement try - except
    #      try:
    #          assert len(self.national_chess_identifier) == 7
    #          assert self.national_chess_identifier[:2].isalpha()
    #          assert self.national_chess_identifier[2:].isnumeric()
    #          return True
    #      except AssertionError:
    #          raise InvalidNationalChessIdentifierFormatException(self.national_chess_identifier)
    #          return False

    # def national_chess_identifier_is_unique(national_chess_dentifier):
    #     """"
    #     Verifies that no other participant has the same national chess identifier
    #     """
    #     # TODO : comparer le identifiant national d'échecs avec les autres identifiants enregistrés
    #     return True


class PlayerList:
    """"
    Player list contained in JSON file
    """
    def __init__(self):
        self.file_path = os.path.abspath("data/players.json")
        self.player_list = []
        self.file_data = {"player_list": self.player_list}

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
            return self.player_list

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
            print('La list de joueurs dans le fichier est vide')
            return self.player_list
        except FileNotFoundError:
            print(f'fichier {self.file_path} inexistant')
            return self.player_list

    def append_player_to_list(self, player):
        """"
        Appends player to memory player_list
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
# ça ne sert pas vraiement ?


class InvalidNationalChessIdentifierFormatException(AssertionError):
    """"
    Exception raised in case of wrong national chess identifier format
    """
    def __init__(self, national_chess_identifier, *args, **kwargs):
        message = f"L'identifiant national d'échecs {national_chess_identifier} est invalide. " \
                  f"Le format doit être de type AA11111"
        super().__init__(message, *args, **kwargs)


def main():
    player_list = PlayerList()
    player_list_data = [
        {
            'first_name': 'Samuel',
            'last_name': 'Prieto',
            'birth_date': '20/04/1990',
            'national_chess_identifier': 'AB12345'
        },
        {
            'first_name': 'Samuel',
            'last_name': 'Prieto',
            'birth_date': '20/04/1990',
            'national_chess_identifier': 'AA12345'
        },
        {
            'first_name': 'Samuel',
            'last_name': 'Prieto',
            'birth_date': '20/04/1990',
            'national_chess_identifier': 'AC12345'
        },
        {
            'first_name': 'Samuel',
            'last_name': 'Prieto',
            'birth_date': '20/04/1990',
            'national_chess_identifier': 'AD12345'
        }
    ]
    with open(player_list.file_path, 'w'):
        pass

    for player in player_list_data:
        first_name = player['first_name']
        last_name = player['last_name']
        birth_date = player['birth_date']
        national_chess_identifier = player['national_chess_identifier']
        new_player = Player(first_name, last_name, birth_date, national_chess_identifier)
        print(new_player)
        new_player.add_player_to_list(player_list)


if __name__ == "__main__":
    main()
