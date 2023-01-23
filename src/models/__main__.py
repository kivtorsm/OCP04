# coding: utf-8
from tournament import Tournament
from player_list import PlayerList
from player import Player


def main():
    tournoi = Tournament("OC", "Toulouse", "20/01/2023", "27/01/2023", "description")
    liste_joueurs = PlayerList()
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

    # Erase tournament data
    with open(tournoi.file_path, 'w'):
        pass

    for player in player_list_data:
        first_name = player['first_name']
        last_name = player['last_name']
        birth_date = player['birth_date']
        national_chess_identifier = player['national_chess_identifier']
        new_player = Player(first_name, last_name, birth_date, national_chess_identifier)
        print(new_player)
        new_player.sign_in_player(liste_joueurs)


if __name__ == "__main__":
    main()
