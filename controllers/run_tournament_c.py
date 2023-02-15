# coding: utf-8

import os

from models.json_file import ProgramData
from models.tournament import Tournament
from models.player import Player

from controllers.program_file_c import ControlProgramFile
from controllers.tournament_c import ControlTournament
from controllers.round_c import ControlRound
from controllers.tournament_player_c import ControlTournamentPlayer

from views.tournament_v import TournamentView
from views.round_v import RoundView


class TournamentController:
    """
    Controller for the running tournament module
    """

    def __init__(self,
                 view: TournamentView,
                 round_view: RoundView,
                 program_file_controls: ControlProgramFile,
                 tournament_controls: ControlTournament,
                 round_controls: ControlRound,
                 tournament_player_controls: ControlTournamentPlayer
                 ):

        # views
        self.view = view
        self.round_view = round_view

        # controllers
        self.program_file_controls = program_file_controls
        self.tournament_controls = tournament_controls
        self.round_controls = round_controls
        self.tournament_player_controls = tournament_player_controls

        # models
        self.program_file = None
        # Initialized in controllers.program_file_controls.charge_program_file

    def create_tournament(self, program_file: ProgramData):
        """
        Runs the creation of a tournament
        :param program_file: program file in which to create the tournament
        :type program_file: ProgramData
        :return: nothing
        :rtype:
        """
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

    def input_national_chess_identifier(self):
        """
        Asks user to input a national chess identifier and checks the input
        format
        :return: national chess identifier after format check
        :rtype: str
        """
        national_chess_identifier_correct = False
        national_chess_identifier = ""
        while not national_chess_identifier_correct:
            try:
                national_chess_identifier \
                    = self.view.prompt_for_national_chess_identifier()
                assert len(national_chess_identifier) == 7
                alpha = national_chess_identifier[:2]
                numeric = national_chess_identifier[2:]
                assert alpha.isalpha()
                assert numeric.isnumeric()
                national_chess_identifier_correct = True
            except AssertionError:
                print("Le format du numéro national d'échecs doit être de "
                      "type AB12345")

        return national_chess_identifier

    def sign_in_players(self, program_file: ProgramData):
        """
        Performs signing phase
        :param program_file: program file in which the program saves data
        :type program_file: ProgramData
        :return: nothing
        :rtype:
        """
        national_chess_identifier = self.input_national_chess_identifier()
        is_already_signed_in = \
            self.tournament_controls.player_already_signed_in_tournament(
                program_file, national_chess_identifier)
        is_player_in_database = \
            self.program_file_controls.is_player_in_database(
                program_file, national_chess_identifier)
        if is_already_signed_in:
            # Check if the player is already signed-in the tournament
            self.view.show_player_already_signed_in(national_chess_identifier)
        else:
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
                self.program_file_controls.add_player(player, program_file)

            # Sign-in player to ongoing tournament and update program file
            self.tournament_controls.sign_in_player(
                program_file, national_chess_identifier)

        # Ask if user wants to add another player
        input_add_new_player = "c"
        while input_add_new_player != "y" and input_add_new_player != "n":
            input_add_new_player = self.view.prompt_for_new_player()
            if input_add_new_player == "y":
                add_new_player = True
                return add_new_player
            elif input_add_new_player == "n":
                add_new_player = False
                return add_new_player

    def run_tournament(self, program_file: ProgramData):
        """
        Runs global tournament module
        :param program_file: program file used to save the program data
        :type program_file: ProgramData
        :return: nothing
        :rtype:
        """
        run_tournament = True
        add_new_player = False
        launch_tournament = False
        tournament = program_file.get_last_tournament()

        while run_tournament:

            if tournament.status == "signing-in players" and add_new_player is False:
                enough_players = self.tournament_controls.does_tournament_has_minimum_number_of_players(program_file)
                even_number_of_players = self.tournament_controls.is_player_count_even(program_file)

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

                if launch_tournament:
                    program_file.start_tournament()
            elif tournament.status == "signing-in players" and \
                    add_new_player is True:
                add_new_player = self.sign_in_players(program_file)
            elif tournament.status == "running":
                self.play_tournament(program_file)
            else:
                break

    def play_current_round(self, program_file: ProgramData):
        """
        Runs ongoing round
        :param program_file: program in which the program data is saved
        :type program_file: ProgramData
        :return: nothing
        :rtype:
        """
        current_round = program_file.get_current_round()
        if current_round.start_datetime == 0:
            self.round_view.prompt_for_start_round(current_round.round_number)
            self.program_file_controls.start_current_round(program_file)
        else:
            is_round_finished = self.round_controls.is_round_finished(program_file)
            if not is_round_finished:
                self.round_controls.set_match_score(program_file)
            else:
                self.program_file_controls.end_current_round(program_file)
                program_file.increase_round_number()

    def play_tournament(self, program_file: ProgramData):
        """
        Runs the playing phase of the tournament
        :param program_file: program file in which program data is saved
        :type program_file: ProgramData
        :return: nothing
        :rtype:
        """
        is_current_round_initialised = self.round_controls.is_current_round_initialised(program_file)
        is_last_round = self.round_controls.is_last_round(program_file)
        if not is_last_round:
            if not is_current_round_initialised:
                self.round_controls.initialise_round(program_file)
            else:
                self.play_current_round(program_file)
        else:
            finished_tournament = program_file.get_last_tournament()
            finished_tournament.status = "finished"
            program_file.update_json_file()
