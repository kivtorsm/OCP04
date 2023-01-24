# coding: utf-8

import random

from tournament import Tournament
from player import Player


def create_tournament():
    tournament = Tournament("OC", "Toulouse", "20/01/2023", "27/01/2023", "description")
    tournament.erase_file_data()
    tournament.write_json_file()
    return tournament


def sign_in_players(tournament):
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
    for player in player_list_data:
        first_name = player['first_name']
        last_name = player['last_name']
        birth_date = player['birth_date']
        national_chess_identifier = player['national_chess_identifier']
        new_player = Player(first_name, last_name, birth_date, national_chess_identifier)
        tournament.sign_in_player(new_player)


def set_couple_list_random(tournament):
    player_list = tournament.get_player_list()
    random.shuffle(player_list)
    couple_list = []
    number_of_matches_per_round = tournament.get_number_of_matches_per_round()
    for match_number in range(0, len(player_list), number_of_matches_per_round):
        couple = [[player_list[match_number], 0], [player_list[match_number+number_of_matches_per_round-1], 0]]
        couple_list.append(couple)
    return couple_list


def round1(tournament):
    couple_list = set_couple_list_random(tournament)
    tournament.update_round_match_list(1, couple_list)


def main():
    # Create data
    tournament = create_tournament()
    sign_in_players(tournament)
    round1(tournament)


if __name__ == "__main__":
    main()
