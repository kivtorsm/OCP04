# coding: utf-8

from models.json_file import ProgramData

from controllers.run_tournament_c import TournamentController
from controllers.reports_c import ReportsController

from views.menu_v import MenuView


class MenuController:
    """
    Controller for set-up and main menu
    """
    def __init__(
            self,
            menu_view: MenuView,
            main_controller: TournamentController,
            reports_controller: ReportsController):

        # Controllers
        self.main_controller = main_controller
        self.reports_controller = reports_controller

        # views
        self.menu_view = menu_view

    def get_main_menu_choice(self, program_status: list):
        """
        Runs the prompt for main manu choice
        :param program_status: program status based on saved data
        :type program_status: list
        :return: user's menu choice
        :rtype: int
        """
        choice = self.menu_view.prompt_for_main_menu_choice(program_status)
        return choice

    def run_main_menu_choice(self, program_file: ProgramData,
                             menu_choice: int):
        """
        Executes program based on decision provided by user in the
        get_menu_choice function
        :param program_file: program file in which program data is saved
        :type program_file: ProgramData
        :param menu_choice: menu choice provided by user
        :type menu_choice: int
        :return: nothing
        :rtype:
        """
        if menu_choice == 0:
            self.main_controller.create_tournament(program_file)
        elif menu_choice == 1:
            self.main_controller.run_tournament(program_file)
        elif menu_choice == 2:
            self.reports_controller.run_player_list_report()
        elif menu_choice == 3:
            self.reports_controller.run_tournament_list_report()
