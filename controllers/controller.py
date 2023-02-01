# coding: utf-8

import os

from models.json_file import ProgramData
from views.view import View


class Controller:

    PROGRAM_FILE_FOLDER_PATH = os.path.abspath(f"./data")
    PROGRAM_FILE_NAME = "chess_tournament_manager.json"
    PROGRAM_FILE_PATH = f"{PROGRAM_FILE_FOLDER_PATH}\\{PROGRAM_FILE_NAME}"

    def __init__(self, view):
        """
        Has a program file and a view
        """
        self.view = view

    def check_program_status(self, program_file: ProgramData):
        """
        Checks if the program file exists and returns a list of booleans indicating:
        1 - if the file is empty
        2 - if there is an ongoing tournament
        3 - inf there is existing report data : tournaments or players
        :return: list of booleans [file_is_empty, ongoing_tournament, existing_report_data]
        :rtype: list
        """
        file_is_empty = True
        ongoing_tournament = False
        existing_report_data = False

        file_is_empty = self.program_file_is_empty()
        if not file_is_empty:
            ongoing_tournament = self.ongoing_tournament(program_file)
            existing_report_data = self.existing_player_data(program_file) or self.existing_tournament_data(program_file)
        result = [file_is_empty, ongoing_tournament, existing_report_data]
        return result

    def charge_program_file(self):
        """
        Creates program file object and gets data from program file if it exists
        :return: programData object with all the current program data in it
        :rtype: ProgramData
        """
        file_exists = os.path.isfile(self.PROGRAM_FILE_PATH)
        if not file_exists:
            # Create file
            with open(self.PROGRAM_FILE_PATH, 'w'):
                pass
            # File created message
            self.view.program_file_created(self.PROGRAM_FILE_PATH)
        else:
            self.view.program_file_already_exists(self.PROGRAM_FILE_PATH)

        # creates ProgramData object with the constant file path
        program_file = ProgramData(self.PROGRAM_FILE_PATH)
        # charges json file data to ProgramData object
        program_file.update_data_object_from_json()

        return program_file

    def program_file_is_empty(self):
        if os.path.getsize(self.PROGRAM_FILE_PATH) == 0:
            self.view.program_file_empty()
            return True
        else:
            return False

    def existing_tournament_data(self, program_file: ProgramData):
        if not program_file.tournament_list:
            return False
        else:
            return True

    def ongoing_tournament(self, program_file: ProgramData):
        result = False
        if self.existing_tournament_data(program_file):
            tournament_list = program_file.tournament_list
            last_tournament = tournament_list[0]
            last_tournament_status = last_tournament.status
            if last_tournament_status == "finished":
                pass
            else:
                result = True
        return result

    def existing_player_data(self, program_file: ProgramData):
        if not program_file.player_dict:
            return False
        else:
            return True

    def get_main_menu_choice(self, program_status: list):
        choice = self.view.prompt_for_main_menu_choice(program_status)
        return choice

    def run_menu_choice(self, menu_choice: int):
        options_list = [

        ]

    def run_tournament(self, tournament_status: str):
        pass

    def run_program(self):
        program_file = self.charge_program_file()
        program_status = self.check_program_status(program_file)
        main_menu_option = self.get_main_menu_choice(program_status)


def main():
    view = View()
    controller = Controller(view)
    program_file = controller.charge_program_file()
    program_status = controller.check_program_status(program_file)
    choice = controller.get_main_menu_choice(program_status)
    print(choice)


if __name__ == "__main__":
    main()
