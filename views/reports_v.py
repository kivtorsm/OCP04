

from models.tournament import Tournament
from models.round import Round

class ReportsView:

    @staticmethod
    def print_table(table):
        print(table)

    @staticmethod
    def show_round_data(tournament_round: Round):
        print(
            f"\n{tournament_round.name.upper()}"
            f"\nDébut : {tournament_round.start_datetime}"
            f"\nFin : {tournament_round.end_datetime}"
        )

    @staticmethod
    def prompt_for_report_menu_choice(program_status):
        existing_player_data = program_status[3]
        existing_tournament_data = program_status[4]
        option = "c"
        print(f"\nBienvenue à la consultation de rapports")
        # if No player data user can consult tournament database
        if not existing_player_data:
            while option not in [str(0), str(1)]:
                print("Veuillez choisir une option :")
                option = input("0 - Revenir au menu principal"
                               "1 - Consulter la base de données des tournois \n")
                try:
                    if int(option) == 0:
                        result = 0
                    elif int(option) == 1:
                        result = 1
                except ValueError:
                    pass
        # if No tournament data user can consult player database
        elif not existing_tournament_data:
            while option not in [str(0), str(1)]:
                print("Veuillez choisir une option :")
                option = input("0 - Revenir au menu principal"
                               "1 - Consulter la base de données des joueurs \n")
                try:
                    if int(option) == 0:
                        result = 0
                    elif int(option) == 1:
                        result = 4
                except ValueError:
                    pass
        # if ongoing_tournament and existing_report_data : carry-on with tournament or consult reports
        else:
            while option not in [str(0), str(1), str(2)]:
                print("Veuillez choisir une option :")
                option = input("0 - Revenir au menu principal\n"
                               "1 - Consulter la base de données des joueurs \n"
                               "2 - Consulter la base de données des tournois \n")
                try:
                    if int(option) == 0:
                        result = 0
                    elif int(option) == 1:
                        result = 4
                    elif int(option) == 2:
                        result = 3
                except ValueError:
                    pass

        return result

    @staticmethod
    def prompt_for_tournament_list_report_choice(tournament_list_length: int):
        option = "c"
        result = "c"

        while option not in [str(0), str(1)]:
            print("Veuillez choisir une option :")
            option = input("0 - Revenir au menu principal\n"
                           "1 - Consulter les détails d'un tournoi \n")
            try:
                if int(option) == 0:
                    result = 0
                elif int(option) == 1:
                    result = 1
            except ValueError:
                pass

        if int(option) == 1:
            option = "c"
            while option not in range(1, int(tournament_list_length) + 1):
                option = input("Veuillez saisir le numéro de tournoi à afficher :\n")
                try:
                    option = int(option)
                    result = int(option)
                except ValueError:
                    pass

        return result

    @staticmethod
    def prompt_for_tournament_details_report_choice():
        option = "c"
        result = "c"

        while option not in [str(0), str(1)]:
            print("Veuillez choisir une option :")
            option = input("0 - Revenir au menu principal\n"
                           "1 - Revenir à la liste des tournois \n")
            try:
                if int(option) in [0, 1]:
                    result = int(option)
            except ValueError:
                pass

        return result

    def show_tournament(self, tournament: Tournament, match_table_list: list):
        print("\n" + "=" * 3 + "TOURNAMENT DETAILS" + "=" * 3)
        print(f"Nom : {tournament.name}")
        print(f"Lieu : {tournament.place}")
        print(f"Dates : du {tournament.start_date} au {tournament.end_date}")
        print(f"Nombre de tours : {tournament.total_rounds}")
        print(f"État : {tournament.get_status_in_french()}")

        round_list = tournament.get_round_list()

        for tournament_round in round_list:
            self.show_round_data(tournament_round)
            print("\n")
            self.print_table(match_table_list[round_list.index(tournament_round)])

    def show_tournament_list(self, tournament_table):
        self.print_table(tournament_table)

    def show_player_list(self, player_table):
        self.print_table(player_table)
