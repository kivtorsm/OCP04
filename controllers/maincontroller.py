# coding: utf-8

import os

from models.json_file import ProgramData
from models.tournament import Tournament
from models.player import Player

from controllers.control_program_file import ControlProgramFile
from controllers.control_tournament import ControlTournament
from controllers.control_round import ControlRound

from views.view import View


class MainController:

    PROGRAM_FILE_FOLDER_PATH = os.path.abspath(f"./data")
    PROGRAM_FILE_NAME = "chess_tournament_manager.json"
    PROGRAM_FILE_PATH = f"{PROGRAM_FILE_FOLDER_PATH}\\{PROGRAM_FILE_NAME}"

    def __init__(self, view, program_file_controls: ControlProgramFile, tournament_controls: ControlTournament, round_controls: ControlRound):
        """
        Has a program file and a view
        """
        # views
        self.view = view

        # controllers
        self.program_file_controls = program_file_controls
        self.tournament_controls = tournament_controls
        self.round_controls = round_controls

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

    def get_national_chess_identifier(self):
        national_chess_identifier_correct = False
        national_chess_identifier = ""
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
        add_new_player = True
        while add_new_player:
            national_chess_identifier = self.get_national_chess_identifier()
            is_already_signed_in = \
                self.tournament_controls.player_already_signed_in_tournament(program_file, national_chess_identifier)
            print(str(is_already_signed_in) + " joueur déjà inscrit")
            try:
                # Check if the player is already signed-in the tournament
                assert is_already_signed_in
                print(f"Le joueur {national_chess_identifier} est déjà inscrit au tournoi")
            except AssertionError:
                # If the player is not signed-in the tournament then check if it already exists in players database
                is_player_in_database = self.program_file_controls.is_player_in_database(program_file,
                                                                                         national_chess_identifier)
                print(str(is_player_in_database) + " jouer en base de données")
                if not is_player_in_database:
                    # ask for player data input
                    player_data = self.view.prompt_for_player_data()
                    player = Player(
                        first_name=player_data['first_name'],
                        last_name=player_data['last_name'],
                        birth_date=player_data['birth_date'],
                        national_chess_identifier=national_chess_identifier
                    )
                    # Add player to the player list in the program file
                    self.program_file_controls.add_player(player)
                # Sign-in player to ongoing tournament and update program file
                self.tournament_controls.sign_in_player(program_file, national_chess_identifier)
            finally:
                # Ask if user wants to add another player
                input_add_new_player = self.view.prompt_for_new_player()
                if input_add_new_player == "y":
                    add_new_player = True
                else:
                    add_new_player = False
                return add_new_player

    def run_tournament(self, program_file: ProgramData):
        run_tournament = True
        add_new_player = False
        launch_tournament = False
        tournament = program_file.get_last_tournament()
        # option_list = [
        #     ["run_tournament=False", "launch_tournament=False", "add_new_player=False"],
        #     ["add_new_player=True"],
        #     ["add_new_player=False", "launch_tournament=True"]
        # ]
        # TODO : question : pourquoi ça ne marche pas
        while run_tournament:
            enough_players = self.tournament_controls.does_tournament_has_minimum_number_of_players(program_file)
            even_number_of_players = self.tournament_controls.is_player_count_even(program_file)
            if tournament.status == "signing-in players":
                # Different menu depending on the evaluation of minimum number of players et total players = even

                if not enough_players or not even_number_of_players:
                    option = self.view.prompt_for_new_player_options()
                else:
                    option = self.view.prompt_for_running_tournament_options()

                if int(option) == 1:
                    run_tournament = False
                    launch_tournament = False
                    add_new_player = False
                elif int(option) == 2:
                    add_new_player = True
                elif int(option) == 3:
                    add_new_player = False
                    launch_tournament = True

                # we execute all commands associated with the chosen option

                # for command in option_list[int(option) - 1]:
                #     exec(command)
                # TODO : demander pourquoi ça ne marche pas

                if add_new_player:
                    self.sign_in_players(program_file)
                elif launch_tournament:
                    program_file.start_tournament()
            elif tournament.status == "running":
                self.play_tournament()

    def play_current_round(self, program_file: ProgramData):
        # TODO : code code code
        pass

    def play_tournament(self, program_file: ProgramData):
        current_round_initialised = self.round_controls.is_current_round_initialised()
        current_round = program_file.get_current_round()
        if not current_round_initialised and current_round == 1:
            self.round_controls.initialise_round1(program_file)
        elif not current_round_initialised and not current_round == 1:
            self.round_controls.initialise_round()
        else:
            self.play_current_round()

    def run_program(self, program_file):
        program_status = self.get_program_status(program_file)
        main_menu_choice = co
        main_menu_option = self.get_main_menu_choice(program_status)
        # TODO : code code code


def main():
    view = View()
    control_program_file = ControlProgramFile()
    control_tournament = ControlTournament()
    control_round = ControlRound
    controller = MainController(
        view=view,
        program_file_controls=control_program_file,
        tournament_controls=control_tournament,
        round_controls=control_round
    )
    program_file = controller.program_file_controls.charge_program_file()
    while True:
        program_status = controller.program_file_controls.evaluate_program_status(program_file)
        main_menu_choice = controller.get_main_menu_choice(program_status)
        controller.run_main_menu_choice(program_file, main_menu_choice)


if __name__ == "__main__":
    main()
