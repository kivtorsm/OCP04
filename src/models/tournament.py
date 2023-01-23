# coding: utf-8

import json
import os


class Tournament:
    """"
    Player list contained in JSON file
    """
    def __init__(self, name, place, start_date, end_date, description, rounds=4):

        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.rounds = rounds
        self.current_round = 0
        self.description = description
        self.round_list = []
        self.player_list = []
        self.file_path = os.path.abspath(f"../data/{self.name}.json")
        self.player_list = []
        self.file_data = {"player_list": self.player_list}

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)
