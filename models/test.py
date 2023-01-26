# coding: utf-8

import random

from tournament import Tournament
from player import Player


def create_tournament():
    """
    Creates tournament with test data
    :return: tournament object
    :rtype: object
    """
    tournament = Tournament("OC", "Toulouse", "20/01/2023", "27/01/2023", "description")
    tournament.erase_file_data()
    tournament.write_json_file()
    return tournament


def sign_in_players(tournament):
    """
    Signs a test data_set of players to a tournament
    :param tournament:
    :type tournament: object
    :return: None
    :rtype: None
    """
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


def set_pair_list_random(tournament):
    """
    Shuffles participant list and creates random pairs returned as a list of pairs to play each other
    :param tournament: a given tournament for which we want to create random pairs
    :type tournament: tournament class
    :return: list of pairs
    :rtype: list
    """
    player_list = tournament.get_player_list()
    # Shuffle player list
    random.shuffle(player_list)
    pair_list = []
    # Get number of player per round
    number_of_matches_per_round = tournament.get_number_of_matches_per_round()
    # For each match, create a pair of players to play each other and add to list
    for match_number in range(0, len(player_list), number_of_matches_per_round):
        # Each pair is a list formed by [player, score]
        pair = [[player_list[match_number], 0], [player_list[match_number+number_of_matches_per_round-1], 0]]
        # The pair (list type) is appended to the global pair list.
        pair_list.append(pair)
    return pair_list


def initialize_round1(tournament):
    """
    Initializes round1 in a given tournament by :
    - Listing pairs of participants that will confront each other
    - Updating the round with the list of pairs
    - Increasing the current round number
    :param tournament: tournament where to initialize round 1
    :type tournament: tournament
    :return: None
    :rtype: None
    """
    # Create randon pair list
    pair_list = set_pair_list_random(tournament)
    # Update the match list in the 1st round of the tournament
    tournament.update_json_round_match_list(1, pair_list)
    # Increase round number
    tournament.increase_round_number()


def play_round1(tournament):
    match_list = tournament.get_round_match_list(1)
    for match in match_list:
        print(match)

def main():
    tournament = create_tournament()
    sign_in_players(tournament)
    initialize_round1(tournament)
    play_round1(tournament)


if __name__ == "__main__":
    main()
