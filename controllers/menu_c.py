# coding: utf-8

from models.json_file import ProgramData

from controllers.control_program_file import ControlProgramFile
from controllers.control_tournament import ControlTournament
from controllers.control_round import ControlRound
from controllers.control_tournament_player import ControlTournamentPlayer
from controllers.tournament_controller import MainController
from controllers.reports_c import ReportsController


from views.view import View
from views.reports_v import ReportsView
from views.round_view import RoundView

from views.menu_view import MenuView


class MenuController:
    def __init__(self, menu_view: MenuView, main_controller: MainController, reports_controller: ReportsController):
        # Controllers
        self.main_controller = main_controller
        self.reports_controller = reports_controller

        # views
        self.menu_view = menu_view

    def get_main_menu_choice(self, program_status: list):
        choice = self.menu_view.prompt_for_main_menu_choice(program_status)
        return choice

    def run_main_menu_choice(self, program_file: ProgramData, menu_choice: int):
        if menu_choice == 0:
            self.main_controller.create_tournament(program_file)
        elif menu_choice == 1:
            self.main_controller.run_tournament(program_file)
        elif menu_choice == 2:
            self.reports_controller.run_player_list_report()
        elif menu_choice == 3:
            self.reports_controller.run_tournament_list_report()


def main():
    view = View()
    round_view = RoundView()
    control_program_file = ControlProgramFile()
    control_tournament = ControlTournament()
    control_round = ControlRound(round_view)
    control_tournament_player = ControlTournamentPlayer()
    tournament_controller = MainController(
        view=view,
        round_view=round_view,
        program_file_controls=control_program_file,
        tournament_controls=control_tournament,
        round_controls=control_round,
        tournament_player_controls=control_tournament_player
    )

    tournament_controller.program_file = tournament_controller.program_file_controls.charge_program_file()

    reports_view = ReportsView()
    reports_controller = ReportsController(tournament_controller.program_file, control_program_file, reports_view)

    menu_view = MenuView()

    menu_controller = MenuController(
        menu_view=menu_view,
        main_controller=tournament_controller,
        reports_controller=reports_controller
    )

    while True:
        program_status = tournament_controller.program_file_controls.evaluate_program_status(tournament_controller.program_file)
        main_menu_choice = menu_controller.get_main_menu_choice(program_status)
        menu_controller.run_main_menu_choice(tournament_controller.program_file, main_menu_choice)


if __name__ == "__main__":
    main()
