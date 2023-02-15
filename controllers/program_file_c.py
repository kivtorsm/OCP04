# coding: utf-8

import os

from models.json_file import ProgramData
from models.player import Player


class ControlProgramFile:
    """
    Program file controller.
    """
    PROGRAM_FILE_FOLDER_PATH = os.path.abspath("./data")
    PROGRAM_FILE_NAME = "chess_tournament_manager.json"
    PROGRAM_FILE_PATH = f"{PROGRAM_FILE_FOLDER_PATH}\\{PROGRAM_FILE_NAME}"
    program_file = None

    def evaluate_program_status(self, program_file: ProgramData):
        """
        Checks if the program file exists and returns a list of booleans
        indicating:
        1 - if the file is empty
        2 - if there is an ongoing tournament
        3 - if there is existing report data : tournaments or players
        4 - if there is existing player reporting data
        5 - if there is existing tournament reporting data
        :return: list of booleans [file_is_empty, ongoing_tournament,
        existing_report_data]
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
                result = [
                    file_is_empty,
                    ongoing_tournament,
                    existing_report_data,
                    existing_player_data,
                    existing_tournament_data]
        except FileNotFoundError as error:
            print(error)
        finally:
            return result

    def charge_program_file(self):
        """
        Creates program file object and gets data from program file if exists
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

        self.program_file = program_file

        return program_file

    def program_file_is_empty(self) -> bool:
        """
        Checks if the program file is empty
        :return: True or false depending on ont the evaluation
        :rtype: bool
        """
        return os.path.getsize(self.PROGRAM_FILE_PATH) == 0

    @staticmethod
    def tournament_data_exists(program_file: ProgramData) -> bool:
        """
        Checks if there is tournament data saved in the program file
        :param program_file: program file where to look for tournament data
        :type program_file: ProgramData
        :return: evaluation for presence of tournament data
        :rtype: bool
        """
        return program_file.tournament_list != 0

    @staticmethod
    def player_data_exists(program_file: ProgramData) -> bool:
        """
        Checks if there is player data saved in the program file
        :param program_file: program file where to look for player data
        :type program_file: ProgramData
        :return: evaluation for presence of player data
        :rtype: bool
        """
        return program_file.player_dict != 0

    def ongoing_tournament_exists(self, program_file: ProgramData) -> bool:
        """
        Checks if there is an existing tournament with non-finished status
        :param program_file: program file where to look for an ongoing
        tournament
        :type program_file: ProgramData
        :return: evaluation for presence of an ongoing tournament
        :rtype: bool
        """
        if self.tournament_data_exists(program_file):
            last_tournament = program_file.get_last_tournament()
            last_tournament_status = last_tournament.status
            return last_tournament_status != "finished"

    @staticmethod
    def is_player_in_database(
            program_file: ProgramData,
            national_chess_identifier: str) -> bool:
        """
        Checks if a player exists in the program player database
        :param program_file: program file where to perform the check
        :type program_file: ProgramData
        :param national_chess_identifier: national chess identifier of the
        player to look for
        :type national_chess_identifier: str
        :return: evaluation for presence of player in database
        :rtype: bool
        """
        player_list = program_file.player_dict.keys()
        result = False
        for player in player_list:
            if player == national_chess_identifier:
                result = True
        return result

    @staticmethod
    def add_player(player: Player, program_file: ProgramData):
        """
        Adds player to the program file database
        :param player: player to be added to the database
        :type player: Player
        :param program_file: program fil in which to add the player
        :type program_file: ProgramData
        :return: nothing
        :rtype:
        """
        program_file.add_player(player)

    @staticmethod
    def start_current_round(program_file: ProgramData):
        """
        Starts the current run by setting the starting time
        :param program_file: program file in which to start the round
        :type program_file: ProgramData
        :return: nothing
        :rtype:
        """
        current_tournament = program_file.get_last_tournament()
        # Set round start time
        current_tournament.set_round_start_time()
        # update ongoing tournament with the start date
        program_file.update_ongoing_tournament(current_tournament)
        # update de json file
        program_file.update_json_file()

    @staticmethod
    def end_current_round(program_file: ProgramData):
        """
        Ends the round by setting the round end datetime after finishing
        all matches
        :param program_file: data file in which to end the round
        :type program_file: ProgramData
        :return: nothing
        :rtype:
        """
        current_tournament = program_file.get_last_tournament()
        current_tournament.set_round_end_time()
        program_file.update_ongoing_tournament(current_tournament)
        program_file.update_json_file()

    def get_number_of_tournaments(self) -> int:
        """
        Returns the number of tournaments existing in the program database
        :return: number of programs in the tournament list of the program
        :rtype: int
        """
        return len(self.program_file.get_tournament_list())
