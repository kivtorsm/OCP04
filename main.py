# coding: utf-8

from controllers.program_file_c import ControlProgramFile
from controllers.tournament_c import ControlTournament
from controllers.round_c import ControlRound
from controllers.tournament_player_c import ControlTournamentPlayer
from controllers.run_tournament_c import TournamentController
from controllers.reports_c import ReportsController
from controllers.menu_c import MenuController

from views.tournament_v import TournamentView
from views.reports_v import ReportsView
from views.round_v import RoundView

from views.menu_v import MenuView


def main():
    """
    Runs the program
    :return: nothing
    :rtype:
    """
    view = TournamentView()
    round_view = RoundView()
    control_program_file = ControlProgramFile()
    control_tournament = ControlTournament()
    control_round = ControlRound(round_view)
    control_tournament_player = ControlTournamentPlayer()
    tournament_controller = TournamentController(
        view=view,
        round_view=round_view,
        program_file_controls=control_program_file,
        tournament_controls=control_tournament,
        round_controls=control_round,
        tournament_player_controls=control_tournament_player
    )

    tournament_controller.program_file \
        = tournament_controller.program_file_controls.charge_program_file()

    reports_view = ReportsView()
    reports_controller = ReportsController(
        tournament_controller.program_file,
        control_program_file,
        reports_view
    )

    menu_view = MenuView()

    menu_controller = MenuController(
        menu_view=menu_view,
        main_controller=tournament_controller,
        reports_controller=reports_controller
    )

    while True:
        program_status = tournament_controller.\
            program_file_controls.\
            evaluate_program_status(tournament_controller.program_file)
        main_menu_choice = menu_controller.get_main_menu_choice(program_status)
        menu_controller.run_main_menu_choice(
            tournament_controller.program_file,
            main_menu_choice
        )


if __name__ == "__main__":
    main()
