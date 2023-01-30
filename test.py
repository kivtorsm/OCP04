# coding: utf-8

import random

from models.tournament import Tournament
from models.player import Player
from models.json_file import ProgramData


def set_up():
    program_file = ProgramData()
    program_file.erase_file_data()
    tournament_list_data = [
        {
            'name': 'super_tournament',
            'place': 'Toulouse',
            'start_date': '20/04/1990',
            'end_date': '20/04/1991',
            'description': 'description',
            'rounds': '4',
            'status': 'finished',
            'current_round': '4',
            'player_list': '[AA12345, AB12345, AC12345, AD12345]'

        },
        {
            'name': 'mega_tournament',
            'place': 'Paris',
            'start_date': '20/04/1995',
            'end_date': '20/04/1996',
            'description': 'description',
            'rounds': '4',
            'status': 'finished',
            'current_round': '4',
            'player_list': '[AA12345, AB12345, AC12345, AD12345]'
        }
    ]
    for tournament_data_dict in tournament_list_data:
        tournament_data = list(tournament_data_dict.values())
        name = tournament_data[0]
        place = tournament_data[1]
        start_date = tournament_data[2]
        end_date = tournament_data[3]
        description = tournament_data[4]
        rounds = int(tournament_data[5])
        status = tournament_data[6]
        current_round = int(tournament_data[7])
        player_list = tournament_data[8].strip('][').split(', ')
        tournament = Tournament(name, place, start_date, end_date, description, player_list, rounds, status,
                                current_round)
        program_file.tournament_list.append(tournament)

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
        program_file.add_player(new_player)
    return program_file


def create_tournament():
    """
    Creates tournament with test data
    :return: tournament object
    :rtype: object
    """
    tournament = Tournament("OC", "Toulouse", "20/01/2023", "27/01/2023", "description", player_list=[])
    return tournament


def sign_in_players(tournament: Tournament, data_file: ProgramData):
    """
    Signs a test data_set of players to a tournament
    :param data_file: program file in which the player list is saved
    :type data_file: ProgramData
    :param tournament: tournament in which we are signing-in the player
    :type tournament: Tournament
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
        data_file.add_player(new_player)


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


def initialize_round1(tournament: Tournament):
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
    tournament.set_round_match_list(1, pair_list)
    # Increase round number
    tournament.increase_round_number()


def play_round1(tournament: Tournament, program_file: ProgramData):
    round_number = 1
    match_list = tournament.get_round_match_list(round_number)
    scores_list = [1, 0.5, 0.5, 0]
    for match_number in range(len(match_list)):
        match = match_list[match_number-1]
        score_player1 = match.match_data[0]
        score_player2 = match.match_data[1]
        score_player1[1] = scores_list[match_number-1]
        score_player2[1] = scores_list[match_number+1]
        tournament.set_score(round_number, match_number, score_player1, score_player2, program_file)


def main():
    program_file = set_up()
    current_tournament = create_tournament()
    program_file.add_new_tournament(current_tournament)
    sign_in_players(current_tournament, program_file)
    initialize_round1(current_tournament)
    play_round1(current_tournament, program_file)
    print(program_file.is_player_in_database('AB12345'))


if __name__ == "__main__":
    main()
