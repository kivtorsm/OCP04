# coding: utf-8

import os

from models.json_file import ProgramData
from models.player import Player


class ControlProgramFile:
    PROGRAM_FILE_FOLDER_PATH = os.path.abspath(f"./data")
    PROGRAM_FILE_NAME = "chess_tournament_manager.json"
    PROGRAM_FILE_PATH = f"{PROGRAM_FILE_FOLDER_PATH}\\{PROGRAM_FILE_NAME}"

    def evaluate_program_status(self, program_file: ProgramData):
        """
        Checks if the program file exists and returns a list of booleans indicating:
        1 - if the file is empty
        2 - if there is an ongoing tournament
        3 - inf there is existing report data : tournaments or players
        :return: list of booleans [file_is_empty, ongoing_tournament, existing_report_data]
        :rtype: list
        """

        result = [True, False, False, False, False]

        try:
            file_is_empty = self.program_file_is_empty()
            ongoing_tournament = self.ongoing_tournament_exists(program_file)
            existing_player_data = self.player_data_exists(program_file)
            existing_tournament_data = self.tournament_data_exists(program_file)
            existing_report_data = existing_player_data or existing_tournament_data

            if not file_is_empty:
                result = [file_is_empty, ongoing_tournament, existing_report_data, existing_player_data, existing_tournament_data]
        except FileNotFoundError as error:
            print(error)
        finally:
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

        # creates ProgramData object with the constant file path
        program_file = ProgramData(self.PROGRAM_FILE_PATH)
        # charges json file data to ProgramData object
        program_file.update_data_object_from_json()

        return program_file

    def program_file_is_empty(self):
        return os.path.getsize(self.PROGRAM_FILE_PATH) == 0

    def tournament_data_exists(self, program_file: ProgramData):
        return program_file.tournament_list != 0

    def player_data_exists(self, program_file: ProgramData):
        return program_file.player_dict != 0

    def ongoing_tournament_exists(self, program_file: ProgramData):
        if self.tournament_data_exists(program_file):
            last_tournament = program_file.get_last_tournament()
            last_tournament_status = last_tournament.status
            return last_tournament_status == "finished"

    def is_player_in_database(self, program_file: ProgramData, national_chess_identifier: str):
        player_list = program_file.player_dict.keys()
        result = False
        for player in player_list:
            if player == national_chess_identifier:
                result = True
        return result

    def add_player(self, player: Player, program_file: ProgramData):
        program_file.add_player(player)

    def start_current_round(self, program_file: ProgramData):
        current_tournament = program_file.get_last_tournament()
        # Set round start time
        current_tournament.set_round_start_time()
        # update ongoing tournament with the start date
        program_file.update_ongoing_tournament(current_tournament)
        # update de json file
        program_file.update_json_file()

    def end_current_round(self, program_file: ProgramData):
        current_tournament = program_file.get_last_tournament()
        current_tournament.set_round_end_time()
        program_file.update_ongoing_tournament(current_tournament)
        program_file.update_json_file()


def main():
    pass


if __name__ == "__main__":
    main()
