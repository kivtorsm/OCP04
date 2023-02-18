
from prettytable import PrettyTable

from models.json_file import ProgramData
from models.tournament import Tournament
from models.round import Round

from controllers.program_file_c import ControlProgramFile

from views.reports_v import ReportsView


class ReportsController:
    """
    Controller for the reporting module
    """
    def __init__(
            self,
            program_file_control: ControlProgramFile,
            reports_view: ReportsView,
            program_file=None):

        # Models
        self.program_file = program_file

        # Controllers
        self.program_file_control = program_file_control

        # views
        self.reports_view = reports_view

    def set_program_file(self, program_file: ProgramData):
        """
        program file update after cross initializations
        :param program_file: program file in which program data is saved
        :type program_file: ProgramData
        :return: nothing
        :rtype:
        """
        self.program_file = program_file

    def create_player_list_table(self) -> PrettyTable:
        """
        Creates and returns a list of players in printing format
        :return: list of players formatted for printing
        :rtype: PrettyTable
        """
        table = PrettyTable()
        player_dict = self.program_file.get_player_dict()
        list_of_players = player_dict.values()
        table.field_names = [
            "# ID échecs",
            "Nom",
            "Prénom",
            "Date de naissance"]
        for player in list_of_players:
            table.add_row(
                [
                    player.national_chess_identifier,
                    player.last_name,
                    player.first_name,
                    player.birth_date
                ]
            )
        return table


    def create_tournament_list_table(self) -> PrettyTable:
        """
        Creates and returns a list of tournaments in printing format
        :return: list of tournaments formatted for printing
        :rtype: PrettyTable
        """
        table = PrettyTable()
        tournament_list = self.program_file.get_tournament_list()
        table.field_names = [
            "#",
            "Nom",
            "Lieu",
            "Date début",
            "Date fin",
            "Rounds",
            "État"]
        for tournament in tournament_list:
            index = tournament_list.index(tournament) + 1
            status_dict = {
                "signing-in players": "Inscriptions joueurs",
                "running": "En cours",
                "finished": "Fini"
            }
            table.add_row(
                [
                    index,
                    tournament.name,
                    tournament.place,
                    tournament.start_date,
                    tournament.end_date,
                    tournament.total_rounds,
                    status_dict[tournament.status]
                ]
            )
        return table

    @staticmethod
    def create_tournament_player_list_table(tournament: Tournament) -> \
            PrettyTable:
        """
        Creates and returns a list of players signed-in a tournament
        in printing format
        :param tournament: tournament for which the player
        list has to be printed
        :type tournament: Tournament
        :return: list of a tournament players formatted for printing
        :rtype: PrettyTable
        """
        table = PrettyTable()
        tournament_player_dict = tournament.get_player_dict()
        tournament_player_list = tournament_player_dict.values()
        table.field_names = ["# ID échecs", "Score"]
        for player in tournament_player_list:
            table.add_row(
                [
                    player.national_chess_identifier,
                    player.score
                ]
            )
        return table

    @staticmethod
    def create_match_list_table(tournament_round: Round):
        """
        Creates and returns a list of matches inside a round of a
        defined tournament
        :param tournament_round: for which the player list has to be printed
        :type tournament_round: Round
        :return: list of a tournament players formatted for printing
        :rtype: PrettyTable
        """
        table = PrettyTable()
        round_match_list = tournament_round.get_match_list()
        table.field_names = [
            "#",
            "Player 1",
            "Score P1",
            "Score P2",
            "Player 2"]
        for match in round_match_list:
            table.add_row(
                [
                    round_match_list.index(match) + 1,
                    match.get_player_national_chess_identifier(0),
                    match.get_player_score(0),
                    match.get_player_score(1),
                    match.get_player_national_chess_identifier(1)
                ]
            )
        return table

    def run_tournament_list_report_menu(self):
        """
        Proposes menu after the tournament list report and generates
        tournament details report
        :return: none
        :rtype:
        """
        # Save number of tournaments
        tournament_list_length = \
            self.program_file_control.get_number_of_tournaments()

        # Ask for user decision : 0 -> main menu, # ->
        # show tournament # details report
        choice = \
            self.reports_view.prompt_for_tournament_list_report_choice(
                tournament_list_length)
        if choice == 0:
            pass
        # when choice is different from 0, generate tournament details report
        else:
            # get the tournament list
            tournament_list = self.program_file.get_tournament_list()

            # get the tournament # in te position # - 1
            tournament = tournament_list[choice - 1]

            # get tournament round list
            tournament_round_list = tournament.get_round_list()
            match_table_list = []

            # for each round, generate a PrettyFormat table with the match data and append it to a list of match tables
            for tournament_round in tournament_round_list:

                # generate PrettyFormat match table
                match_table = self.create_match_list_table(tournament_round)

                # append table to match table list
                match_table_list.append(match_table)

            # generate the tournament player list for the ranking
            tournament_player_list = self.create_tournament_player_list_table(tournament)

            # show tournament details report
            self.reports_view.show_tournament(tournament, match_table_list, tournament_player_list)

    def run_player_list_report(self):
        """
        Launches the player list report
        :return: none
        :rtype:
        """
        player_table = self.create_player_list_table()
        self.reports_view.show_player_list_alphabetically(player_table)

    def run_tournament_list_report(self):
        """
        Launches the tournament list report
        :return:
        :rtype:
        """
        tournament_list_table = self.create_tournament_list_table()
        self.reports_view.show_tournament_list(tournament_list_table)
        self.run_tournament_list_report_menu()
