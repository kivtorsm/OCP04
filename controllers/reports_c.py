
from prettytable import PrettyTable

from models.json_file import ProgramData
from models.tournament import Tournament
from models.round import Round

from controllers.control_program_file import ControlProgramFile

from views.reports_v import ReportsView


class ReportsController:
    def __init__(self, program_file: ProgramData, program_file_control: ControlProgramFile, reports_view: ReportsView):

        # Models
        self.program_file = program_file

        # Controllers
        self.program_file_control = program_file_control

        # views
        self.reports_view = reports_view

    def create_player_list_table(self):
        table = PrettyTable()
        player_dict = self.program_file.get_player_dict()
        list_of_players = player_dict.values()
        table.field_names = ["# ID échecs", "Nom", "Prénom", "Date de naissance"]
        for player in list_of_players:
            table.add_row(
                [
                    player.national_chess_identifier,
                    player.last_name,
                    player.first_name,
                    player.birth_date
                ]
            )
        table.get_string(sortby="Nom")
        return table

    def create_tournament_list_table(self):
        table = PrettyTable()
        tournament_list = self.program_file.get_tournament_list()
        table.field_names = ["#", "Nom", "Lieu", "Date début", "Date fin", "Rounds", "État"]
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
    def create_tournament_player_list_table(tournament: Tournament):
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
        table = PrettyTable()
        round_match_list = tournament_round.get_match_list()
        table.field_names = ["#", "Player 1", "Score P1", "Score P2", "Player 2"]
        for match in round_match_list:
            table.add_row(
                [
                    round_match_list.index(match),
                    match.get_player_national_chess_identifier(0),
                    match.get_player_score(0),
                    match.get_player_score(1),
                    match.get_player_national_chess_identifier(1)
                ]
            )
        return table

    def choose_tournament_details_report(self):
        tournament_list_length = self.program_file_control.get_number_of_tournaments()
        choice = self.reports_view.prompt_for_tournament_list_report_choice(tournament_list_length)
        print(choice)
        print(type(choice))
        if choice == 0:
            pass
        else:
            print(choice)
            tournament_list = self.program_file.get_tournament_list()
            tournament = tournament_list[choice - 1]
            tournament_round_list = tournament.get_round_list()
            match_table_list = []
            for tournament_round in tournament_round_list:
                match_table = self.create_match_list_table(tournament_round)
                match_table_list.append(match_table)
            self.reports_view.show_tournament(tournament, match_table_list)
            # choice = self.run_tournament_details_report_menu_choice()

    def run_player_list_report(self):
        player_table = self.create_player_list_table()
        self.reports_view.show_player_list(player_table)

    def run_tournament_list_report(self):
        choice = "c"
        tournament_list_table = self.create_tournament_list_table()
        self.reports_view.show_tournament_list(tournament_list_table)
        self.choose_tournament_details_report()
        # while choice not in [str(0), str(1)]:
        #     choice = self.reports_view.prompt_for_tournament_list_report_choice()
        #     if choice == 0:
        #         pass
        #     elif choice == 1:
        #         self.run_tournament_details_report_menu_choice()

    # def run_tournament_details_report_menu_choice(self):
    #     choice = "c"
    #     while choice not in [0, 1]:
    #         choice = self.reports_view.prompt_for_tournament_details_report_choice()
    #     return int(choice)
