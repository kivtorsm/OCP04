# coding: utf-8

import os

from models.json_file import ProgramData
from models.tournament import Tournament
from models.player import Player
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

    def get_program_status(self, program_file: ProgramData):
        """
        Checks if the program file exists and returns a list of booleans indicating:
        1 - if the file is empty
        2 - if there is an ongoing tournament
        3 - inf there is existing report data : tournaments or players
        :return: list of booleans [file_is_empty, ongoing_tournament, existing_report_data]
        :rtype: list
        """
        ongoing_tournament = False
        existing_report_data = False
        file_is_empty = self.program_file_is_empty()
        if not file_is_empty:
            ongoing_tournament = self.ongoing_tournament_exists(program_file)
            existing_report_data = self.player_data_exists(program_file) or self.tournament_data_exists(program_file)
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

    def tournament_data_exists(self, program_file: ProgramData):
        if not program_file.tournament_list:
            return False
        else:
            return True

    def get_last_tournament(self, program_file: ProgramData):
        tournament_list = program_file.tournament_list
        last_tournament = tournament_list[0]
        return last_tournament

    def ongoing_tournament_exists(self, program_file: ProgramData):
        result = False
        if self.tournament_data_exists(program_file):
            last_tournament = self.get_last_tournament(program_file)
            last_tournament_status = last_tournament.status
            if not last_tournament_status == "finished":
                result = True
        return result

    def player_data_exists(self, program_file: ProgramData):
        if not program_file.player_dict:
            return False
        else:
            return True

    def get_main_menu_choice(self, program_status: list):
        choice = self.view.prompt_for_main_menu_choice(program_status)
        return choice

    def run_main_menu_choice(self, program_file, menu_choice: int):
        options_list = [
            "self.create_tournament(program_file)",
            "self.run_tournament(program_file)",
            "self.get_report_menu_choice()"
        ]
        option_choice = options_list[menu_choice]
        eval(option_choice)

    def create_tournament(self, program_file: ProgramData):
        tournament_data = self.view.prompt_for_tournament_creation()
        tournament = Tournament(
            tournament_data['name'],
            tournament_data['place'],
            tournament_data['start_date'],
            tournament_data['end_date'],
            tournament_data['description'],
            rounds=tournament_data['rounds']
        )
        program_file.add_new_tournament(tournament)
        self.run_tournament(program_file)

    def get_report_menu_choice(self):
        # TODO : code code code
        pass

    def already_signed_in_tournament(self, program_file: ProgramData, national_chess_identifier: str):
        tournament = program_file.tournament_list[0]
        player_list = tournament.player_list
        if national_chess_identifier in player_list:
            return True
        else:
            return False

    def get_national_chess_identifier(self):
        national_chess_identifier_correct = False
        while not national_chess_identifier_correct:
            try:
                national_chess_identifier = self.view.prompt_for_national_chess_identifier()
                assert len(national_chess_identifier) == 7
                alpha = national_chess_identifier[:2]
                numeric = national_chess_identifier[2:]
                assert alpha.isalpha()
                assert numeric.isnumeric()
                national_chess_identifier_correct = True
            except AssertionError:
                print("Le format du numéro national d'échecs doit être de type AB12345")
                # TODO : pas censé être ici le print ?

        return national_chess_identifier

    def sign_in_players(self, program_file: ProgramData):
        national_chess_identifier = self.get_national_chess_identifier()
        is_already_signed_in = self.already_signed_in_tournament(program_file, national_chess_identifier)
        try:
            assert is_already_signed_in
            print(f"Le joueur {national_chess_identifier} est déjà inscrit au tournoi")
        except AssertionError:
            is_player_in_database = program_file.is_player_in_database(national_chess_identifier)
            if not is_player_in_database:
                player_data = self.view.prompt_for_player_data()
                player = Player(
                    first_name=player_data['first_name'],
                    last_name=player_data['last_name'],
                    birth_date=player_data['birth_date'],
                    national_chess_identifier=national_chess_identifier
                )
                program_file.add_player(player)
            tournament = self.get_last_tournament(program_file)
            tournament.sign_in_player(national_chess_identifier)
            program_file.update_ongoing_tournament(tournament)

    def run_tournament(self, program_file: ProgramData):
        tournament = self.get_last_tournament(program_file)
        if tournament.status == "signing-in players":
            self.sign_in_players(program_file)
        else:
            self.play_tournament()

    def play_tournament(self):
        # TODO : code code code
        pass

    def run_program(self, program_file):
        program_status = self.get_program_status(program_file)
        main_menu_choice = co
        main_menu_option = self.get_main_menu_choice(program_status)
        # TODO : code code code


def main():
    view = View()
    controller = Controller(view)
    program_file = controller.charge_program_file()
    while True:
        program_status = controller.get_program_status(program_file)
        main_menu_choice = controller.get_main_menu_choice(program_status)
        controller.run_main_menu_choice(program_file, main_menu_choice)


if __name__ == "__main__":
    main()
