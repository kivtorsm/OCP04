import json
import os
from json import JSONEncoder
import ast

class Player:

    def __init__(self, first_name, last_name, birth_date, national_chess_identifier):

        # TODO: tester le format du national_chess_identifier
        # TODO: tester que le national_chess_identifier est bien unique ou du moins différent des autres connus
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.national_chess_identifier = national_chess_identifier
        # assert self.date_has_right_format()
        # assert self.national_chess_identifier_has_right_format()
        # assert self.national_chess_identifier_is_unique()

    def __str__(self):
        return f"Le jouer {self.first_name} {self.last_name} est né le {self.birth_date} et son identifiant national " \
               f"d'échecs est le {self.national_chess_identifier}"

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

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))

class PlayerList:
    """"
    Player list contained in JSON file
    """
    def __init__(self):
        self.file_path = os.path.abspath("data/players.json")
        print(self.file_path)
        self.player_dict = {}
        self.player_list = []

    def append_player(self, player):
        """
        Adds player to json player list.

        Parameters
        -------
        self
        player

        Returns
        -------
        None
        """

        player_json_data = self.player_to_jsondata(player)
        print(f"Le joueur à ajouter est {player_json_data}")
        # TODO: évaluer chemin d'accès pour qu'on puisse y accéder quel que soit l'emplacement de lancement
        try:
            with open(self.file_path, "r+") as outfile:
                if os.stat(self.file_path).st_size == 0:
                    print('File is empty')
                    outfile.write(player_json_data)
                    print(f"Player data successfully saved")
                else:
                    print('File is not empty')
                    file_data = json.load(outfile)
                    print(f"le fichier contient {file_data}")
                    print(type(file_data))
                    file_data.update(player_json_data)
                    print(file_data)
                    outfile.write(file_data)
                    print(f"Player {self} data successfully saved")
        except FileNotFoundError:
            print("Fichier non trouvé ou inexistant ou alors tu m'as donné le mauvais chemin d'accès")



    def player_to_jsondata(self, player):
        """
        Transforms player data into Json format data.

        Parameters
        -------
        self
        player

        Returns
        -------
        str
            str with player data in Json format
        """

        try:
            with open(self.file_path, "r") as file:
                file_data = json.load(file)
                print(type(file_data))
                for json_player in file_data:
                    print(type(json_player))
                    print(f"le fichier contient {json_player}")
                    for player in json_player:
                        print(player)
            with open(self.file_path, "r+") as file:
                player_list.append(player.to_json())
                json.dump(self.player_list, file, indent=4, cls=MyEncoder)
                print(f"Player {player.first_name} {player.last_name} data successfully saved")
        except json.JSONDecodeError as error:
            print(error)
            with open(self.file_path, "w") as file:
                # Initialising player list
                # Json main object will be player list with list of players inside
                self.player_list.append(player.to_json())
                self.player_dict = {"player_list": self.player_list}
                json.dump(self.player_dict, file, indent=4, cls=MyEncoder)


class MyEncoder(JSONEncoder):
    """"
    Returns dictionary with data in JSON format
    """

    def default(self, o):
        return o.__dict__


class InvalidNationalChessIdentifierFormatException(AssertionError):
    """"
    Exception raised in case of wrong national chess identifier format
    """
    def __init__(self, national_chess_identifier, *args, **kwargs):
        message = f"L'identifiant national d'échecs {national_chess_identifier} est invalide. " \
                  f"Le format doit être de type AA11111"
        super().__init__(message, *args, **kwargs)


if __name__ == "__main__":

    p1 = Player("Samuel", "Prieto", "20/04/1990", "AB12345")
    print(p1)
    p2 = Player("Samuel", "Prieto", "20/04/1990", "AA12345")
    print(p2)
    p3 = Player("Samuel", "Prieto", "20/04/1990", "AC12345")
    print(p3)
    p4 = Player("Samuel", "Prieto", "20/04/1990", "AD12345")
    print(p4)
    # Initialisation de la liste de joeurs
    player_list = PlayerList()

    # Ajout de la liste de joueurs
    player_list.player_to_jsondata(p1)
    player_list.player_to_jsondata(p2)
    player_list.player_to_jsondata(p3)
    player_list.player_to_jsondata(p4)
