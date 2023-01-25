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
        self.file_path = os.path.abspath(f"../data/{self.name}.json")
        # TODO : adapt depending on execution

    def __str__(self):
        with open(self.file_path, "r") as file:
            data = json.load(file)
        return json.dumps(data, default=lambda o: o.__dict__, indent=4)

    def to_json(self):
        """
        Returns tournament object as a json string
        :return: tournament object as a json str
        :rtype: str
        """
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def increase_round_number(self):
        """
        Increases the current round count
        :return: None
        :rtype: Nonve
        """
        self.current_round =+ 1

    def erase_file_data(self):
        """
        Erases tournament json file data
        :return: None
        :rtype: None
        """
        with open(self.file_path, 'w'):
            pass

    def write_json_file(self):
        """
        Updates json tournament file
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

    def sign_in_player(self, player):
        """
        Signs-in the tournament a given player
        :param player: player to be signed-in the tournament
        :type player: player
        :return: None
        :rtype: None
        """
        self.add_player_to_player_dict(player)
        self.write_json_file()

    def get_data_from_json_file(self):
        """
        Updates tournament object with json file data and returns it as an object
        :return: file_data
        :rtype: dict
        """
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

    def add_player_to_player_dict(self, player):
        """
        Adds player to the tournament player dict
        :param player: player to be added to the tournament
        :type player: player
        :return: None
        :rtype: None
        """
        self.player_dict[player.national_chess_identifier] = player

    def get_number_of_players(self):
        """
        Returns the number of players signed-in the tournament
        :return: Number of signed-in players
        :rtype: int
        """
        return len(self.player_dict)

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
        return int(self.get_number_of_players()/2)

    def get_player_list(self):
        """
        Returns the list of players signed-in the tournament
        :return: list of signed-in players
        :rtype: list
        """
        # self.get_player_dict_from_json()
        player_list = list(self.player_dict.keys())
        return player_list

    def get_round_list(self):
        """
        Returns the list of rounds to be played in the tournament
        :return: list of rounds to be played in the tournament
        :rtype: list
        """
        self.get_data_from_json_file()
        return self.round_list

    def update_round_match_list(self, round_number, match_list):
        """
        Updates the list of matches of a given round with a new given list of matches
        :param round_number: the round number where to update the list of matches
        :type round_number: int
        :param match_list: the updated list of matches to set in the round match list
        :type match_list: list
        :return: None
        :rtype: None
        """
        self.get_data_from_json_file()
        # create round object
        tournament_round = Round(round_number)
        # update round with json data
        tournament_round.download_round_data(self, round_number)
        # update round with input match_list
        tournament_round.initialize_match_list(self, match_list)
        # update tournament with round object
        self.round_list[round_number-1] = json.loads(tournament_round.to_json())
        # update json file
        self.write_json_file()

    def get_round_data(self, round_number):
        """
        Returns a given round data
        :param round_number: number of the round for which to get the data
        :type round_number: int
        :return: round data
        :rtype: dict
        """
        round_data = self.round_list[round_number-1]
        return round_data

    def get_round_match_list(self, round_number):
        """
        Returns the match list from a specific round
        :param round_number: the round number for which we want the list of matches
        :type round_number: int
        :return: list of matches for a specified round
        :rtype: list
        """
        tournament_round = Round(round_number)
        match_list = tournament_round.get_match_list(self, round_number)
        return match_list

