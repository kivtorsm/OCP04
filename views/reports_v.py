
from prettytable import PrettyTable

from models.tournament import Tournament
from models.round import Round


class ReportsView:
    """
    Reports module view
    """
    @staticmethod
    def print_table(table: PrettyTable):
        """
        Prints a table given in parameters
        :param table: table to be printed given
        :type table: PrettyTable
        :return: No return
        :rtype: Empty
        """
        print(table)

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

    def show_tournament(self, tournament: Tournament, match_table_list: list):
        """
        Prints tournament details with all round details and math lists.
        :param tournament: tournament to be shown
        :type tournament: Tournament
        :param match_table_list: list of tables with all matches for each round
        :type match_table_list: list
        :return: no return
        :rtype:
        """
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
            self.print_table(
                match_table_list[round_list.index(tournament_round)])

    def show_tournament_list(self, tournament_table: PrettyTable):
        """
        Prints the list of tournaments in the database as a table.
        :param tournament_table: table containing the list of tournaments
        formatted for printing
        :type tournament_table: PrettyTable
        :return: None
        :rtype:
        """
        self.print_table(tournament_table)

    def show_player_list(self, player_table: PrettyTable):
        """
        Prints the list of players in the database as a table.
        :param player_table: table containing the list of tournaments
        formatted for printing
        :type player_table: PrettyTable
        :return: None
        :rtype:
        """
        self.print_table(player_table)
