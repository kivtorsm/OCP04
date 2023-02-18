
from prettytable import PrettyTable

from models.tournament import Tournament
from models.round import Round


class ReportsView:
    """
    Reports module view
    """
    @staticmethod
    def show_round_data(tournament_round: Round):
        """
        Prints round data
        :param tournament_round: tournament round to be printed
        :type tournament_round: Round
        :return: Empty
        :rtype:
        """
        print(
            f"\n{tournament_round.name.upper()}"
            f"\nDébut : {tournament_round.start_datetime}"
            f"\nFin : {tournament_round.end_datetime}"
        )

    @staticmethod
    def prompt_for_tournament_list_report_choice(
            tournament_list_length: int) -> int:
        """
        Menu after listing all tournaments. Allows user to consult details of
        a tournament or to go back to main menu
        :param tournament_list_length: length of the tournament list in the
        database. Allows control of the input choice
        :type tournament_list_length: int
        :return: Menu choice : 0 -> main menu, # -> tournament number to show
        :rtype: int
        """
        result = "c"
        incorrect_input_value = True

        while incorrect_input_value:
            option = input("\nVeuillez saisir le numéro du tournoi à "
                           "consulter ou 0 pour revenir au menu principal\n")
            try:
                result = int(option)
                if result in range(0, int(tournament_list_length) + 1):
                    incorrect_input_value = False
            except ValueError:
                print("Veuillez saisir un nombre entier dans la limite du "
                      "nombre de tournois affichés")
        return result

    def show_tournament(self, tournament: Tournament, match_table_list: list, tournament_player_table: PrettyTable):
        """
        Prints tournament details with all round details and math lists.
        :param tournament_player_table: tournament player table for showing the tournament ranking
        :type tournament_player_table:
        :param tournament: tournament to be shown
        :type tournament: Tournament
        :param match_table_list: list of tables with all matches for each round
        :type match_table_list: list
        :return: no return
        :rtype:
        """
        # Print tournament data

        print("\n" + "=" * 3 + "DÉTAILS DU TOURNOI" + "=" * 3)
        print(f"Nom : {tournament.name}")
        print(f"Lieu : {tournament.place}")
        print(f"Dates : du {tournament.start_date} au {tournament.end_date}")
        print(f"Nombre de tours : {tournament.total_rounds}")
        print(f"État : {tournament.get_status_in_french()}")

        round_list = tournament.get_round_list()

        # Print ranking
        print("\n" + ">" * 3 + "CLASSEMENT" + "<" * 3)
        self.show_player_list_by_score(tournament_player_table)

        # For each tournament round
        for tournament_round in round_list:

            # print round data
            self.show_round_data(tournament_round)

            # print match table
            print(
                match_table_list[round_list.index(tournament_round)])

    @staticmethod
    def show_tournament_list(tournament_table: PrettyTable):
        """
        Prints the list of tournaments in the database as a table.
        :param tournament_table: table containing the list of tournaments
        formatted for printing
        :type tournament_table: PrettyTable
        :return: None
        :rtype:
        """
        print(tournament_table)

    @staticmethod
    def show_player_list_alphabetically(player_table: PrettyTable):
        """
        Prints the list of players in the database as a table sorted alphabetically
        :param player_table: table containing the list of tournaments formatted for printing
        :type player_table: PrettyTable
        :return: None
        :rtype:
        """
        print(player_table.get_string(sortby='# ID échecs'))

    @staticmethod
    def show_player_list_by_score(player_table: PrettyTable):
        """
        Prints the list of players in the database as a table sorted by score (ranking table)
        :param player_table: table containing the list of tournaments formatted for printing
        :type player_table: PrettyTable
        :return: None
        :rtype:
        """
        print(player_table.get_string(sortby='Score', reversesort=True))
